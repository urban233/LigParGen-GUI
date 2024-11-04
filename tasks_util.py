import os
import pathlib
import shutil
import subprocess
from urllib import request


class Constants:
  """Class that contains constants used throughout the setup."""
  # <editor-fold desc="Class attributes">
  project_root_path = pathlib.Path(__file__).parent.absolute()
  """The root path of the project."""

  wsl2_source_path = pathlib.Path(project_root_path, "src", "python", "ligpargen_gui", "model", "wsl2")
  """The path of the wsl2 source directory."""

  wsl2_source_build_path = pathlib.Path(project_root_path, "deployment", "src", "bin", "_internal", "src", "python", "ligpargen_gui", "model", "wsl2")
  """The path of the wsl2 source directory in the build folder."""

  dos_2_unix_filepath = pathlib.Path(project_root_path, "external", "dos2unix.exe")
  """The filepath to the dos2unix exe file."""

  build_output_path: pathlib.Path = pathlib.Path(project_root_path, "_build", "output")
  """The path to the build output directory."""

  podman_build_dir = pathlib.Path(project_root_path, "deployment", "podman")
  """The path to the build directory of the WSL2 distro rootfs."""

  alma_linux_rootfs_filename: str = "alma9-ligpargen-rootfs.tar"
  """The name of the AlmaLinux rootfs."""

  alma_linux_rootfs_build_filepath: pathlib.Path = pathlib.Path(
    project_root_path, "deployment", "podman", alma_linux_rootfs_filename
  )
  """The filepath of the AlmaLinux rootfs."""

  alma_linux_rootfs_filepath: pathlib.Path = pathlib.Path(
    project_root_path, "deployment", "src", "offline_resources", alma_linux_rootfs_filename
  )
  """The filepath of the AlmaLinux rootfs."""

  alma_linux_rootfs_url: str = "https://w-hs.sciebo.de/s/q5oYjcZdEzCDyEH/download"
  """The url for downloading the AlmaLinux rootfs."""

  post_installation_runner_project_path = pathlib.Path(
    project_root_path, "src", "c_sharp", "PostInstallationRunner"
  )
  """The path to the PostInstallationRunner C# project."""

  post_installation_runner_publish_xml_filepath = pathlib.Path(
    project_root_path, "src", "c_sharp", "PostInstallationRunner",
    "Properties", "PublishProfiles", "FolderProfile.pubxml"
  )
  """The filepath to the PostInstallationRunner publishing profile."""

  post_installation_runner_exe_build_filepath = pathlib.Path(
    project_root_path, "src", "c_sharp", "PostInstallationRunner",
    "bin", "Release", "net8.0", "publish", "win-x64", "PostInstallationRunner.exe"
  )
  """The filepath to the PostInstallationRunner published .exe file."""

  post_installation_runner_exe_filepath = pathlib.Path(
    project_root_path, "deployment", "src", "PostInstallationRunner.exe"
  )
  """The filepath to the PostInstallationRunner .exe file that is used in the inno setup script."""

  wsl_check_project_path = pathlib.Path(
    project_root_path, "src", "c_sharp", "PostInstallationRunner"
  )
  """The path to the WslCheck C# project."""

  wsl_check_publish_xml_filepath = pathlib.Path(
    project_root_path, "src", "c_sharp", "WslCheck",
    "Properties", "PublishProfiles", "FolderProfile.pubxml"
  )
  """The filepath to the WslCheck publishing profile."""

  wsl_check_exe_build_filepath = pathlib.Path(
    project_root_path, "src", "c_sharp", "WslCheck",
    "bin", "Release", "net8.0", "publish", "win-x64", "WslCheck.exe"
  )
  """The filepath to the WslCheck published .exe file."""

  wsl_check_exe_filepath = pathlib.Path(
    project_root_path, "deployment", "src", "WslCheck.exe"
  )
  """The filepath to the WslCheck .exe file that is used in the inno setup script."""

  spec_file_for_pyinstaller_filepath = pathlib.Path(
    project_root_path, "deployment", "pyinstaller", "main.spec"
  )
  """The filepath for the spec file used for the PyInstaller build."""

  inno_setup_compiler_filepath = "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
  """The filepath of the compiler executable of inno setup."""

  inno_setup_script_filepath: pathlib.Path = pathlib.Path(project_root_path, "deployment", "setup.iss")
  """The filepath of the inno setup script."""

  inno_setup_update_script_filepath: pathlib.Path = pathlib.Path(project_root_path, "deployment", "update_setup.iss")
  """The filepath of the inno setup script."""
  # </editor-fold>


class Directory:
  """Container for common filesystem directory-based operations."""

  @staticmethod
  def exists(a_path: str | pathlib.Path) -> bool | None:
    """Checks if the given directory exists.

    Args:
      a_path: The path to the directory.

    Returns:
      A boolean indicating whether the directory exists or not or None if the argument is illegal.
    """
    # <editor-fold desc="Checks">
    if a_path is None or a_path == "":
      return False

    # </editor-fold>

    return pathlib.Path(a_path).exists()

  @staticmethod
  def create_directory(a_path: str | pathlib.Path) -> pathlib.Path | None:
    """Creates a directory and all its subdirectories.

    Args:
      a_path: The path to the directory to be deleted.

    Returns:
      The path that was created or None if the directory could not be deleted or the argument was illegal.

    Notes:
      This static method always deletes the directory if it already exists.
    """
    # <editor-fold desc="Checks">
    if a_path is None or a_path == "":
      return None

    # </editor-fold>

    tmp_path: pathlib.Path = pathlib.Path(a_path)
    if not Directory.purge(tmp_path):
      return None
    tmp_path.mkdir(parents=True)
    return tmp_path

  @staticmethod
  def copy_directory(source_directory_name: str | pathlib.Path,
                     destination_directory_name: str | pathlib.Path) -> bool:
    """Copies a directory and all its contents to a new location.

    Args:
      source_directory_name: The path to the directory to be copied.
      destination_directory_name: The path to the destination directory.

    Returns:
      A boolean indicating the success of the operation.
    """
    # <editor-fold desc="Checks">
    if source_directory_name is None or source_directory_name == "":
      return False
    if destination_directory_name is None or destination_directory_name == "":
      return False

    # </editor-fold>

    try:
      tmp_source_dir = pathlib.Path(source_directory_name)
      tmp_destination_dir = pathlib.Path(destination_directory_name)

      if not Directory.purge(tmp_destination_dir):
        return False
      if not tmp_destination_dir.exists():
        tmp_destination_dir.mkdir(parents=True)

      shutil.copytree(tmp_source_dir, tmp_destination_dir, dirs_exist_ok=True)
      return True
    except Exception as e:
      return False

  @staticmethod
  def purge(a_path: str | pathlib.Path) -> bool:
    """Deletes a directory and all its contents.

    This function can also be used if the directory might not exist because
    it checks the existence before purging.

    Args:
      a_path: The path to the directory to be deleted.

    Returns:
      A boolean indicating the success of the operation.
    """
    # <editor-fold desc="Checks">
    if a_path is None or a_path == "":
      return False

    # </editor-fold>

    try:
      tmp_path = pathlib.Path(a_path)
      if tmp_path.exists():
        shutil.rmtree(tmp_path)
    except Exception as e:
      return False
    return True


class File:
  """Container for common filesystem file-based operations."""

  @staticmethod
  def copy(a_source_file_name: str | pathlib.Path, a_dest_file_name: str | pathlib.Path, overwrite: bool = False) -> bool:
    """Copies a file to a new location.

    Args:
      a_source_file_name: The path of the file to copy.
      a_dest_file_name: The destination path of the file to copy.
      overwrite: A boolean indicating whether the file should be overwritten.

    Returns:
      A boolean indicating the success of the operation.
    """
    # <editor-fold desc="Checks">
    if a_source_file_name is None or a_source_file_name == "":
      return False
    if a_dest_file_name is None or a_dest_file_name == "":
      return False
    if overwrite is None:
      return False

    # </editor-fold>

    try:
      if overwrite:
        if pathlib.Path(a_dest_file_name).exists():
          os.remove(a_dest_file_name)
      shutil.copy(a_source_file_name, pathlib.Path(a_dest_file_name))
    except Exception as e:
      return False
    return True

  @staticmethod
  def delete(a_filepath: str | pathlib.Path) -> bool:
    """Deletes a file.

    Args:
      a_filepath: The path of the file to delete.

    Returns:
      A boolean indicating the success of the operation.
    """
    # <editor-fold desc="Checks">
    if a_filepath is None or a_filepath == "":
      return False

    # </editor-fold>

    try:
      os.remove(a_filepath)
    except Exception as e:
      print(e)
      return False
    return True


def download_file(an_url: str, a_filepath: str) -> bool:
  """Downloads a single file of the given URL.

  Args:
    an_url: The URL to download.
    a_filepath: The path to the file to download.

  Returns:
    True if the download was successful, False otherwise.
  """
  try:
    request.urlretrieve(an_url, a_filepath)
    return True
  except Exception as e:
    print(e)
    return False


class InvokePowerShell:
  """Container class for powershell specific methods."""

  @staticmethod
  def run_command(a_cmd, a_cwd):
    """Runs a single command in the powershell."""
    subprocess.run(["powershell", "-Command", a_cmd], shell=True, cwd=a_cwd)
