import os

from ligpargen_gui.model.util import safeguard


def check_file_exists_in_wsl(a_distro_name: str, a_linux_path: str) -> bool:
  """Checks if a given linux path exists in a WSL2 distro

  Args:
    a_distro_name: The distro name.
    a_linux_path: The linux path.

  Returns:
    True if the path exists, Otherwise: False
  """
  # <editor-fold desc="Checks">
  safeguard.CHECK(a_distro_name is not None)
  safeguard.CHECK(a_linux_path is not None)
  # </editor-fold>
  windows_path = f"\\\\wsl$\\{a_distro_name}\\{a_linux_path.lstrip('/')}"
  return os.path.exists(windows_path)


def windows_to_wsl_path(windows_path: str) -> str:
  """Convert a Windows path to a Linux-style WSL path.

  Args:
    windows_path (str): The Windows file path (e.g., "C:\\Users\\username\\file.txt").

  Returns:
    str: The Linux-style WSL path (e.g., "/mnt/c/Users/username/file.txt").
  """
  # <editor-fold desc="Checks">
  safeguard.CHECK(windows_path is not None)
  # </editor-fold>
  # Replace the backslashes with forward slashes
  linux_path = windows_path.replace("\\", "/")
  # Extract the drive letter and replace with /mnt/<drive>
  if len(linux_path) > 1 and linux_path[1] == ':':
    drive_letter = linux_path[0].lower()
    linux_path = f"/mnt/{drive_letter}{linux_path[2:]}"
  return linux_path
