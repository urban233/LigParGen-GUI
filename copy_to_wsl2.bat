set "sourceDirectory=%USERPROFILE%\github_repos\LigParGen-GUI\src\python\ligpargen_gui\model\wsl2"
set "destinationDirectory=\\wsl.localhost\alma9LigParGen0205\home\alma_ligpargen\ligpargen_gui\wsl2"
rmdir /s /q "%destinationDirectory%"
xcopy "%sourceDirectory%" "%destinationDirectory%" /s /e /i /h
