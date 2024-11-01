import os


def check_file_exists_in_wsl(a_distro_name: str, a_linux_path: str):
  """Checks if a given linux path exists in a WSL2 distro"""
  windows_path = f"\\\\wsl$\\{a_distro_name}\\{a_linux_path.lstrip('/')}"
  return os.path.exists(windows_path)
