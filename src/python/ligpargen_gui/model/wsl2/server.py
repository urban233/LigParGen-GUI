import glob
import json
import os.path
import pathlib
import shutil
import subprocess
import zmq
from wsl2 import constants, utils


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
    tmp_input_folder: str = self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER]
    tmp_input_folder = tmp_input_folder.replace("C:\\Users", "/mnt/c/Users")
    tmp_input_folder = tmp_input_folder.replace("\\", "/")
    self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER] = tmp_input_folder
    tmp_output_folder: str = self.job_input_data[constants.JobInputDataKeys.OUTPUT_FOLDER]
    tmp_output_folder = tmp_output_folder.replace("C:\\Users", "/mnt/c/Users")
    tmp_output_folder = tmp_output_folder.replace("\\", "/")
    self.job_input_data[constants.JobInputDataKeys.OUTPUT_FOLDER] = tmp_output_folder

  def run_job(self) -> bool:
    # <editor-fold desc="Preperations">
    tmp_utils = utils.Utils()
    if not tmp_utils.prepare_folder_structure():
      return False
    if not tmp_utils.copy_pdb_files_to_wsl2(self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER]):
      return False
    # </editor-fold>
    for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_DIR, "*.pdb"):
      if not self.run_ligpargen_command(pathlib.Path(tmp_file)):
        print(f"LigParGen conversion of {tmp_file} failed!")
    # <editor-fold desc="Post-processing">
    if not tmp_utils.filter_results(self.job_input_data[constants.JobInputDataKeys.RESULT_FILE_TYPES]):
      return False
    # </editor-fold>
    return True

  def run_ligpargen_command(self, a_file: pathlib.Path) -> bool:
    try:
      subprocess.run(
        ["bash", str(constants.Paths.LIGPARGEN_BATCH_FILEPATH),
         "-i", str(a_file),
         "-n", str(a_file).replace(a_file.suffix, ""),
         # "-p", f"{self.job_input_data['output_folder']}/{tmp_filename}",  # IMPORTANT: Directory gets cleaned before result files are generated!!!
         # "-p", tmp_filename,
         "-c", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOLECULE_CHARGE]),
         "-o", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOL_OPT_ITER]),
         "-cgen", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_CHARGE_MODEL])],
        cwd=str(constants.Paths.SCRATCH_DIR)  # The cwd needs to be set to ensure that the temporarily files of ligpargen are stored there!
      )
      return True
    except Exception as e:
      print(e)  # TODO: Add logger message here
      return False

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
