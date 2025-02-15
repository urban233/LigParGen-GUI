@echo off
setlocal

rem Define source and destination directories
set "sourceDirectory=C:\ProgramData\IBCI\LigParGenGUI\bin\_internal\src\python\ligpargen_gui\model\wsl2"
set "destinationDirectory=\\wsl.localhost\almaLigParGen9\home\alma_ligpargen\ligpargen_gui\wsl2"
set "logFile=%~dp0CopyFilesLog.txt"

rem Define WSL details for chmod operation
set "distroName=almaLigParGen9"
set "username=alma_ligpargen"
set "targetFilePath=/home/alma_ligpargen/ligpargen_gui/wsl2/start_server.sh"

rem Function to log messages with timestamps
set timestamp=[%date% %time%]

echo %timestamp% - Script started. >> "%logFile%"

rem Check if destination directory exists and delete it if it does
if exist "%destinationDirectory%" (
    echo %timestamp% - Attempting to remove existing destination directory: %destinationDirectory% >> "%logFile%"
    rmdir /s /q "%destinationDirectory%"
    if %errorlevel% equ 0 (
        echo %timestamp% - Successfully removed existing destination directory. >> "%logFile%"
    ) else (
        echo %timestamp% - Failed to remove existing destination directory. >> "%logFile%"
        goto :error
    )
) else (
    echo %timestamp% - Destination directory does not exist, no need to remove. >> "%logFile%"
)

rem Copy all files and subdirectories from source to destination
echo %timestamp% - Attempting to copy files from %sourceDirectory% to %destinationDirectory% >> "%logFile%"
xcopy "%sourceDirectory%" "%destinationDirectory%" /s /e /i /h /y
if %errorlevel% equ 0 (
    echo %timestamp% - Files copied successfully from %sourceDirectory% to %destinationDirectory%. >> "%logFile%"
) else (
    echo %timestamp% - An error occurred during the file copy operation. >> "%logFile%"
    goto :error
)

rem Run chmod +x in WSL for the specified file
echo %timestamp% - Attempting to set execute permissions on %targetFilePath% in WSL >> "%logFile%"
wsl -d %distroName% -u %username% sudo chmod +x %targetFilePath%
if %errorlevel% equ 0 (
    echo %timestamp% - Execute permissions set successfully on %targetFilePath%. >> "%logFile%"
) else (
    echo %timestamp% - Failed to set execute permissions on %targetFilePath%. >> "%logFile%"
    goto :error
)

wsl -d %distroName% -u %username% sudo chown -R alma_ligpargen:alma_ligpargen /home/alma_ligpargen/ligpargen_gui
if %errorlevel% equ 0 (
    echo %timestamp% - Change ownership successfully on %targetFilePath%. >> "%logFile%"
) else (
    echo %timestamp% - Failed to change ownership on %targetFilePath%. >> "%logFile%"
    goto :error
)

echo %timestamp% - Script completed successfully. >> "%logFile%"
goto :eof

:error
echo %timestamp% - Script completed with errors. Check the log file for details. >> "%logFile%"
exit /b 1
