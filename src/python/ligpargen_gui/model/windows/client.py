import json
import pathlib
import subprocess

import zmq
from PyQt6 import QtCore

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import filesystem_util, powershell


class Client(QtCore.QObject):
  # <editor-fold desc="Class attributes">
  progress_signal = QtCore.pyqtSignal(tuple)
  """Custom signal to transfer the progress."""
  # </editor-fold>

  def __init__(self):
    # Socket definitions
    super().__init__()
    context = zmq.Context()
    self._sender_socket = context.socket(zmq.PUSH)
    self._sender_socket.connect("tcp://127.0.0.1:8033")
    self._recv_socket = context.socket(zmq.PULL)
    self._recv_socket.connect("tcp://127.0.0.1:8034")
    self.job_status = ""

  def send_job_input(self, a_job_input_as_json: str):
    self._sender_socket.send_json(a_job_input_as_json)

  def copy_results(self, a_dest_folder: pathlib.Path):
    tmp_output_folder: str = filesystem_util.windows_to_wsl_path(str(a_dest_folder))
    tmp_wsl_log_path: str = filesystem_util.windows_to_wsl_path(str(model_definitions.ModelDefinitions.DEFAULT_WSL2_LOG_PATH))
    powershell.await_run_wsl_command(
      ["cp", "-r", "/home/alma_ligpargen/ligpargen_gui/scratch/results/*", f"{tmp_output_folder}"]
    )
    powershell.await_run_wsl_command(
      ["cp", "-r", "/home/alma_ligpargen/ligpargen_gui/logs/*", tmp_wsl_log_path]
    )

  def check_progress_status(self):
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
