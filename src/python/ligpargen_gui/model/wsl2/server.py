import glob
import json
import os.path
import pathlib
import subprocess
import zmq


class Server:
  def __init__(self):
    # Socket definitions
    context = zmq.Context()
    self._recv_socket = context.socket(zmq.PULL)
    self._recv_socket.bind("tcp://127.0.0.1:8033")
    self._sender_socket = context.socket(zmq.PUSH)
    self._sender_socket.bind("tcp://127.0.0.1:8034")
    self.job_input_data: dict = {}

  def listen_for_job_input(self):
    self.job_input_data: dict = json.loads(self._recv_socket.recv_json())
    tmp_input_folder: str = self.job_input_data["input_folder"]
    tmp_input_folder = tmp_input_folder.replace("C:\\Users", "/mnt/c/Users")
    tmp_input_folder = tmp_input_folder.replace("\\", "/")
    self.job_input_data["input_folder"] = tmp_input_folder
    tmp_output_folder: str = self.job_input_data["output_folder"]
    tmp_output_folder = tmp_output_folder.replace("C:\\Users", "/mnt/c/Users")
    tmp_output_folder = tmp_output_folder.replace("\\", "/")
    self.job_input_data["output_folder"] = tmp_output_folder

  def run_job(self):
    for tmp_file in glob.glob(os.path.join(self.job_input_data["input_folder"], "*.pdb")):
      self.run_ligpargen_command(pathlib.Path(tmp_file))

  def run_ligpargen_command(self, a_file: pathlib.Path):
    tmp_filename = str(a_file).replace(a_file.suffix, "")
    subprocess.run(
      ["bash", "/home/alma_ligpargen/ligpargen_batch",
       "-i", str(a_file),
       "-n", tmp_filename,
       # "-p", f"{self.job_input_data['output_folder']}/{tmp_filename}",  # IMPORTANT: Directory gets cleaned before result files are generated!!!
       "-p", tmp_filename,
       "-c", str(self.job_input_data["options"]["molecule_charge"]),
       "-o", str(self.job_input_data["options"]["mol_opt_iter"]),
       "-cgen", str(self.job_input_data["options"]["charge_model"])]
    )

  def ligpargen_command(self):
    subprocess.run(
      ["bash", "/home/alma_ligpargen/ligpargen_batch",
       "-s", "CCO",
       "-n", "Acy",
       "-p", "tmp_results/",  # IMPORTANT: Directory gets cleaned before result files are generated!!!
       "-c", "0",
       "-o", "3",
       "-cgen", "CM1A-LBCC"]
    )
