import json
import pathlib
import subprocess

import zmq
from PyQt6 import QtCore

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import filesystem_util, powershell, safeguard


class Client(QtCore.QObject):
  """Class for communicating with the server in the WSL2."""
  # <editor-fold desc="Class attributes">
  progress_signal = QtCore.pyqtSignal(tuple)
  """Custom signal to transfer the progress."""
  # </editor-fold>

  def __init__(self) -> None:
    """Constructor."""
    # Socket definitions
    super().__init__()
    context = zmq.Context()
    self._sender_socket = context.socket(zmq.PUSH)
    self._sender_socket.connect("tcp://127.0.0.1:8033")
    self._recv_socket = context.socket(zmq.PULL)
    self._recv_socket.connect("tcp://127.0.0.1:8034")
    self.job_status = ""

  def send_job_input(self, a_job_input_as_json: str) -> None:
    """Sends the job as JSON string to the server.

    Args:
      a_job_input_as_json: The input JSON string to be sent to the server.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_job_input_as_json is not None)
    # </editor-fold>
    self._sender_socket.send_json(a_job_input_as_json)

  def copy_results(self, a_dest_folder: pathlib.Path) -> bool:
    """Copies the results from the WSL2 filesystem to the Windows filesystem.

    Args:
      a_dest_folder: The destination folder where the results will be copied to.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_dest_folder is not None)
    safeguard.CHECK(a_dest_folder.exists())
    # </editor-fold>
    tmp_output_folder: str = filesystem_util.windows_to_wsl_path(str(a_dest_folder))
    tmp_wsl_log_path: str = filesystem_util.windows_to_wsl_path(str(model_definitions.ModelDefinitions.DEFAULT_WSL2_LOG_PATH))
    powershell.await_run_wsl_command(
      ["cp", "-r", "/home/alma_ligpargen/ligpargen_gui/logs/*", tmp_wsl_log_path]
    )
    return powershell.await_run_wsl_command(
      ["cp", "-r", "/home/alma_ligpargen/ligpargen_gui/scratch/results/*", f"{tmp_output_folder}"]
    )

  def check_progress_status(self) -> None:
    """Checks the progress of a job running in the WSL2."""
    tmp_progress_info: dict = {"status": "started"}
    while tmp_progress_info["status"] != "finished" or tmp_progress_info["status"] != "failed":
      tmp_progress_info: dict = json.loads(self._recv_socket.recv_json())
      self.progress_signal.emit(tuple(tmp_progress_info.values()))
      if tmp_progress_info["status"] == "failed":
        self.job_status = "failed"
        break
      elif tmp_progress_info["status"] == "finished":
        self.job_status = "finished"
        break
