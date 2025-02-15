REM Setup WSL2 distro
wsl --import almaLigParGen9 "C:\ProgramData\IBCI\wsl2\LigParGenGUI" "C:\ProgramData\IBCI\LigParGenGUI\tmp\alma9-ligpargen-rootfs.tar"
if not exist C:\ProgramData\IBCI\wsl2\LigParGenGUI\ext4.vhdx exit -1
