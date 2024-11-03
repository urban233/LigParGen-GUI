import pathlib
import subprocess
from invoke import task
import tasks_util


@task()
def rootfs(c, version: str = "", check_version=False):
  try:
    tmp_cwd = tasks_util.Constants.podman_build_dir
    if check_version:
      tasks_util.InvokePowerShell.run_command("podman images", tmp_cwd)
    tmp_commands = [
      "podman machine start",
      f"podman build -f .\DOCKERFILE -t alma9_ligpargen:version",
      f"podman run --name almaLigParGen alma9_ligpargen:version",
      "podman export -o alma9-ligpargen-rootfs.tar almaLigParGen"
    ]
    for tmp_cmd in tmp_commands:
      tasks_util.InvokePowerShell.run_command(tmp_cmd, tmp_cwd)
  except Exception as e:
    print(e)
  finally:
    print("Rootfs build process finished.")


@task()
def build(c, rootfs=False, post_installation_runner=False, wsl_check=False):
  try:
    # Build & move rootfs to inno setup src dir
    if rootfs:
      tmp_cwd = tasks_util.Constants.podman_build_dir
      tasks_util.Directory().copy_directory(tasks_util.Constants.wsl2_source_path, tasks_util.Constants.wsl2_source_podman_path)
      tmp_commands = [
        "podman machine start",
        "podman build -f .\DOCKERFILE -t alma9_ligpargen:1.0.0.0",
        "podman run --name almaLigParGen alma9_ligpargen:1.0.0.0",
        "podman export -o alma9-ligpargen-rootfs.tar almaLigParGen",
        "podman rm almaLigParGen",
        "podman rmi alma9_ligpargen:1.0.0.0"
      ]
      for tmp_cmd in tmp_commands:
        tasks_util.InvokePowerShell.run_command(tmp_cmd, tmp_cwd)
      tasks_util.File().copy(
        tasks_util.Constants.alma_linux_rootfs_build_filepath,
        tasks_util.Constants.alma_linux_rootfs_filepath, overwrite=True
      )
      tasks_util.File().delete(
        tasks_util.Constants.alma_linux_rootfs_build_filepath
      )
    else:
      # Download any necessary offline resources
      # <editor-fold desc="Check local availability of AlmaLinux dependency">
      if not pathlib.Path.exists(tasks_util.Constants.alma_linux_rootfs_filepath):
        print("AlmaLinux distro does not exist for deployment. Please re-run build with -r or --rootfs flag.")
        return
        # print(f"Downloading {tasks_util.Constants.alma_linux_rootfs_filename} ...")
        # if not tasks_util.download_file(tasks_util.Constants.alma_linux_rootfs_url,
        #                                 str(tasks_util.Constants.alma_linux_rootfs_filepath)):
        #   print(f"Unable to download {tasks_util.Constants.alma_linux_rootfs_filename}, build process exists.")
        #   return
        # print(f"Finished downloading {tasks_util.Constants.alma_linux_rootfs_filename}.")
      # </editor-fold>
    # Build & move PostInstallationRunner
    if post_installation_runner:
      tmp_cwd = tasks_util.Constants.project_root_path
      tmp_cmd = f"dotnet publish {tasks_util.Constants.post_installation_runner_project_path} /p:PublishProfile={tasks_util.Constants.post_installation_runner_publish_xml_filepath}"
      tasks_util.InvokePowerShell.run_command(tmp_cmd, tmp_cwd)
      tasks_util.File().copy(tasks_util.Constants.post_installation_runner_exe_build_filepath,
                             tasks_util.Constants.post_installation_runner_exe_filepath, overwrite=True)
    if wsl_check:
      tmp_cwd = tasks_util.Constants.project_root_path
      tmp_cmd = f"dotnet publish {tasks_util.Constants.wsl_check_project_path} /p:PublishProfile={tasks_util.Constants.wsl_check_publish_xml_filepath}"
      tasks_util.InvokePowerShell.run_command(tmp_cmd, tmp_cwd)
      tasks_util.File().copy(tasks_util.Constants.wsl_check_exe_build_filepath,
                             tasks_util.Constants.wsl_check_exe_filepath, overwrite=True)
    # Build & move LigParGenGUI (with PyInstaller)
    tasks_util.Directory().purge(pathlib.Path(tasks_util.Constants.project_root_path, "deployment", "src", "bin"))
    c.run(f"pyinstaller {tasks_util.Constants.spec_file_for_pyinstaller_filepath} --distpath deployment/src -y")
    # Build inno setup .exe
    subprocess.run(
      [
        tasks_util.Constants.inno_setup_compiler_filepath,
        str(tasks_util.Constants.inno_setup_script_filepath)
      ]
    )
    tasks_util.Directory().purge(pathlib.Path(tasks_util.Constants.project_root_path, "deployment", "src", "bin"))
  except Exception as e:
    print(e)
  finally:
    # Clean directory
    print("Build process finished.")
