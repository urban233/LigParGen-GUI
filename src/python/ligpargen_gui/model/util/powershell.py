import logging
import subprocess

from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.preference import model_definitions

logger = default_logging.setup_logger(__file__)


def await_run_wsl_command(a_cmd: list) -> bool:
  """Runs a wsl command and waits for it to finish."""
  tmp_cmd = ["wsl", "-d", model_definitions.ModelDefinitions.DISTRO_NAME, "-u", "alma_ligpargen"]
  tmp_cmd += a_cmd
  tmp_complete_process = subprocess.run(tmp_cmd)
  if tmp_complete_process.returncode != 0:
    default_logging.append_to_log_file(logger, "Error: Usage or syntax error occurred.", logging.ERROR)
    default_logging.append_to_log_file(logger, f"Error output: {tmp_complete_process.stderr}", logging.ERROR)
    return False
  return True


def async_run_wsl_command(a_cmd: list):
  """Runs asynchronously a wsl command."""
  subprocess.Popen(
    ["wsl", "-d", model_definitions.ModelDefinitions.DISTRO_NAME, "-u", "alma_ligpargen", a_cmd],
    creationflags=subprocess.CREATE_NO_WINDOW
  )
