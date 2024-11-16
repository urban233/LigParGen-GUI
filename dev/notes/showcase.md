# Software Showcase 14.11.2024

## Location of test files
C:\Users\student\user_space\projects\ligpargen_gui\test_files

## Location of boss.tar.gz
C:\Users\student\user_space\projects\ligpargen\Deployment\boss0824.tar.gz

## Prerequisites for boss installation
1. Uninstall Boss with the command:
wsl -d almaLigParGen9 -u alma_ligpargen rm -r /home/alma_ligpargen/boss

2. Start LigParGenGUI and choose the .tar.gz file to install


## Deployment
Done completely with Inno Setup:
- Import of WSL2 distro
- Copy all relevant files for ligpargen gui pyqt application
- Run post-installation task to move relevant files into the WSL2

Inno Setup does NOT check if WSL2 is installed!
