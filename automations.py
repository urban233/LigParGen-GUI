"""
#A* -------------------------------------------------------------------
#B* This file contains source code for running automation tasks related
#-* to the build process of the LigParGen-GUI computer program
#C* Copyright 2025 by Martin Urban.
#D* -------------------------------------------------------------------
#E* It is unlawful to modify or remove this copyright notice.
#F* -------------------------------------------------------------------
#G* Please see the accompanying LICENSE file for further information.
#H* -------------------------------------------------------------------
#I* Additional authors of this source file include:
#-*
#-*
#-*
#Z* -------------------------------------------------------------------
"""
import argparse
import pathlib
import subprocess
import shutil
import sys
import time
import automation_util

PROJECT_ROOT_DIR = pathlib.Path(__file__).parent

PYTHON_EXECUTABLE = sys.executable  # This gives the current Python executable
DEBUG = True


# <editor-fold desc="Automation classes">
class BuildInnoSetup:
  """Contains the logic for building the inno setup EXE file."""

  def __init__(self) -> None:
    """Constructor."""
    self.inno_build_path = pathlib.Path(PROJECT_ROOT_DIR / "inno-build-release")
    self.inno_build_assets_path = pathlib.Path(self.inno_build_path / "inno-assets")
    self.inno_build_cache_path = pathlib.Path(self.inno_build_path / "inno-cache")
    self.inno_sources_build_path = pathlib.Path(self.inno_build_path / "inno-sources")
    self.inno_build__internal_path = pathlib.Path(self.inno_sources_build_path / "bin/_internal")
    self.inno_build_prerequisite_path = pathlib.Path(self.inno_sources_build_path / "prerequisite")
    self.inno_build_third_party_path = pathlib.Path(self.inno_sources_build_path / "third_party")
    self.inno_build_tmp_path = pathlib.Path(self.inno_sources_build_path / "tmp")
    self.inno_setup_script_path = pathlib.Path(PROJECT_ROOT_DIR / "deployment/src/inno_setup")
    self.inno_setup_script_filepath = pathlib.Path(PROJECT_ROOT_DIR / "deployment/src/inno_setup" / "setup.iss")
    self.inno_setup_compiler_filepath = pathlib.Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe")
    self.pyinstaller_filepath = pathlib.Path(PROJECT_ROOT_DIR / ".venv/Scripts" / "pyinstaller.exe")
    self.pyinstaller_spec_filepath = pathlib.Path(PROJECT_ROOT_DIR / "deployment/pyinstaller" / "main.spec")

  def setup_build_environment(self, include_wsl2_distro: bool = False) -> None:
    """Sets up a temporary build environment.

    Args:
      include_wsl2_distro: A boolean flag whether the wsl2 distro should be included or not (in the inno setup EXE)
    """
    # <editor-fold desc="Path/Filepath definitions">
    tmp_pyssa_win_build_logo_filepath = pathlib.Path(PROJECT_ROOT_DIR / "assets/convert_logo_to_ico" / "logo.ico")
    tmp_vc_redist_setup_filepath = pathlib.Path(PROJECT_ROOT_DIR / "third_party/microsoft" / "VC_redist.x64.exe")
    tmp_windows_tasks_exe_filepath = pathlib.Path(PROJECT_ROOT_DIR / "deployment/offline_resources" / "WindowsTasks.exe")
    # </editor-fold>
    """IMPORTANT
    Use the python interpreter of the venv of pymol windows build because
    that interpreter gets also used in the build script of the 
    pymol windows build repo!
    """
    # <editor-fold desc="Restore build directory for new build">
    if self.inno_build_assets_path.exists():
      shutil.rmtree(self.inno_build_assets_path)
    if self.inno_sources_build_path.exists():
      shutil.rmtree(self.inno_sources_build_path)
    self.inno_build_path.mkdir(exist_ok=True)
    self.inno_build_assets_path.mkdir()
    self.inno_sources_build_path.mkdir()
    self.inno_build_cache_path.mkdir(exist_ok=True)
    # </editor-fold>
    # <editor-fold desc="Get WSL2 distro from sciebo">
    pathlib.Path(self.inno_build_tmp_path).mkdir()
    if include_wsl2_distro:
      if not pathlib.Path.exists(pathlib.Path(self.inno_build_cache_path / "alma9-ligpargen-rootfs.tar")):
        print("alma9-ligpargen-rootfs.tar not found! If you have a TAR file move it to inno-build-release/inno-cache.")
        return

      if not automation_util.File.copy(
        pathlib.Path(self.inno_build_cache_path / "alma9-ligpargen-rootfs.tar"),
        pathlib.Path(self.inno_build_tmp_path / "alma9-ligpargen-rootfs.tar"),
      ):
        print("Copying the alma9-ligpargen-rootfs.tar failed!")
        return
    # </editor-fold>
    # <editor-fold desc="Compile Python sources to EXE file">
    if pathlib.Path(PROJECT_ROOT_DIR / "dist").exists():
      shutil.rmtree(pathlib.Path(PROJECT_ROOT_DIR / "dist"))
    subprocess.run(
      [self.pyinstaller_filepath, self.pyinstaller_spec_filepath],
      stdout=sys.stdout, stderr=sys.stderr, text=True
    )
    automation_util.Directory.copy_directory(
      pathlib.Path(PROJECT_ROOT_DIR / "dist/bin"),
      pathlib.Path(self.inno_sources_build_path / "bin")
    )
    # </editor-fold>
    # <editor-fold desc="Copy operations">
    automation_util.Directory.copy_directory(
      pathlib.Path(PROJECT_ROOT_DIR / "assets"),
      pathlib.Path(self.inno_build__internal_path / "assets")
    )
    automation_util.File.copy(
      pathlib.Path(PROJECT_ROOT_DIR / "LICENSE"),
      pathlib.Path(self.inno_build__internal_path / "LICENSE"),
      overwrite=True
    )
    automation_util.File.copy(
      pathlib.Path(PROJECT_ROOT_DIR / "README.md"),
      pathlib.Path(self.inno_build__internal_path / "README.md"),
      overwrite=True
    )
    # TODO: Add automated way of updating the version number project wide
    # Note: Until now there are different locations where the versions are stored
    # (1) constants.py (2) pyproject.toml (3) version_history.json
    # => TODO: This has to change for better maintenance!
    automation_util.File.copy(
      pathlib.Path(PROJECT_ROOT_DIR / "version_history.json"),
      pathlib.Path(self.inno_build__internal_path / "version_history.json"),
      overwrite=True
    )
    automation_util.File.copy(
      pathlib.Path(PROJECT_ROOT_DIR / "deployment/scripts/batch" / "setup.bat"),
      pathlib.Path(self.inno_build_tmp_path / "setup.bat"),
      overwrite=True
    )
    automation_util.File.copy(
      pathlib.Path(PROJECT_ROOT_DIR / "deployment/scripts/batch" / "update.bat"),
      pathlib.Path(self.inno_build_tmp_path / "update.bat"),
      overwrite=True
    )

    self.inno_build_third_party_path.mkdir(exist_ok=True)
    self.inno_build_prerequisite_path.mkdir(exist_ok=True)
    shutil.copy(tmp_vc_redist_setup_filepath, pathlib.Path(self.inno_build_third_party_path / "VC_redist.x64.exe"))
    self.inno_build_assets_path.mkdir(exist_ok=True)
    shutil.copy(tmp_pyssa_win_build_logo_filepath, pathlib.Path(self.inno_build_assets_path / "logo.ico"))
    # </editor-fold>

  def build(self, an_inno_script_path: pathlib.Path) -> None:
    """Builds the PyMOL Windows EXE file.

    Args:
      an_inno_script_path: A filepath to the inno script to compile
    """
    try:
      tmp_start_time = time.time()
      subprocess.run(
        [self.inno_setup_compiler_filepath, an_inno_script_path],
        stdout=sys.stdout, stderr=sys.stderr, text=True
      )
      tmp_end_time = time.time()
      tmp_duration = tmp_end_time - tmp_start_time
      print(f"The build process of the inno setup EXE took: {tmp_duration:.2f} seconds ({(tmp_duration/60):.2f} minutes).")
    except Exception as e:
      print(e)
# </editor-fold>


# <editor-fold desc="Automation functions">
def build_setup_exe() -> None:
  """Builds the inno setup EXE file."""
  try:
    tmp_builder = BuildInnoSetup()
    tmp_builder.setup_build_environment(
      include_wsl2_distro=True,
    )
    tmp_builder.build(tmp_builder.inno_setup_script_filepath)
  except Exception as tmp_exception:
    print(tmp_exception)
    return


def build_update_src_only_exe() -> None:
  """Builds the update src only inno setup EXE file."""
  try:
    tmp_builder = BuildInnoSetup()
    tmp_builder.setup_build_environment()
    tmp_builder.build(
      pathlib.Path(tmp_builder.inno_setup_script_path / "setup_only_src.iss")
    )
  except Exception as tmp_exception:
    print(tmp_exception)
    return


def clean_build_setup_exe() -> None:
  """Cleans the inno setup build directory."""
  shutil.rmtree(pathlib.Path(PROJECT_ROOT_DIR / "inno-build-release"))
# </editor-fold>


def main() -> None:
  """Main function."""
  parser = argparse.ArgumentParser(description="Automation script with subcommands.")
  # <editor-fold desc="Subparsers">
  subparsers = parser.add_subparsers(dest='command')
  build_setup_exe_parser = subparsers.add_parser('build-setup-exe', help="Builds the inno setup EXE file.")
  build_setup_exe_parser.set_defaults(func=build_setup_exe)
  build_update_src_only_exe_parser = subparsers.add_parser('build-update-src-exe', help="Builds update src the inno setup EXE file.")
  build_update_src_only_exe_parser.set_defaults(func=build_update_src_only_exe)
  clean_build_setup_exe_parser = subparsers.add_parser('clean', help="Cleans the inno setup build directory.")
  clean_build_setup_exe_parser.set_defaults(func=clean_build_setup_exe)
  # </editor-fold>
  args = parser.parse_args()

  if args.command:
    args.func()


if __name__ == "__main__":
  main()
