Podman LigParGen Build Guide
============================

Build process
-------------
cwd: D:\user_space\ligpargen_offline
podman build -f .\DOCKERFILE -t alma9_ligpargen:0.1.0.1
podman run --name almaLigParGen alma9_ligpargen:0.1.0.1
podman export -o alma9-ligpargen-rootfs.tar almaLigParGen
wsl --import almaLigParGen9 storage\ .\alma9-ligpargen-rootfs.tar

Useful podman commands
----------------------
List all podman containers
podman ps -a

Remove a podman container
podman rm <container_name>

Start a podman container with a terminal
podman run --name test2 -it ubuntu_ligpargen:0.2.0.2

Install BOSS
------------------
COPY boss0824.tar.gz LigParGen-CommandFiles-master.zip /home/alma_ligpargen/BOSS_FILES/
RUN chown -R alma_ligpargen:alma_ligpargen ./BOSS_FILES/
RUN tar -xvf ./BOSS_FILES/boss0824.tar.gz && echo 'export BOSSdir=/home/alma_ligpargen/boss' >> ~/.bashrc
