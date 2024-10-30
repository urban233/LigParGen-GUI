import pathlib
import subprocess

import zmq


class Client:
  def __init__(self):
    # Socket definitions
    context = zmq.Context()
    self._sender_socket = context.socket(zmq.PUSH)
    self._sender_socket.connect("tcp://127.0.0.1:8033")
    self._recv_socket = context.socket(zmq.PULL)
    self._recv_socket.connect("tcp://127.0.0.1:8034")

  def send_job_input(self, a_job_input_as_json: str):
    self._sender_socket.send_json(a_job_input_as_json)

  def copy_results(self, a_dest_folder: pathlib.Path):
    tmp_output_folder: str = str(a_dest_folder)
    tmp_output_folder = tmp_output_folder.replace("C:\\Users", "/mnt/c/Users")
    tmp_output_folder = tmp_output_folder.replace("\\", "/")
    subprocess.run(
      [
        "wsl",
        "-d",
        "alma9LigParGen0205",
        "-u",
        "alma_ligpargen",
        "cp",
        "-r",
        "/home/alma_ligpargen/ligpargen_gui/scratch/results/*",
        f"{tmp_output_folder}",
      ],
      check=True,
    )

  def wait_for_results(self):
    print(self._recv_socket.recv_json())
