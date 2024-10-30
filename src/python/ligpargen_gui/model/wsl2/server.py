import glob
import json
import logging
import os.path
import pathlib
import shutil
import subprocess
import zmq
from wsl2 import constants, utils
from wsl2 import post_processing
from wsl2 import default_logging, exception

logger = default_logging.setup_logger(__file__)


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
    # <editor-fold desc="Preparations">
    tmp_utils = utils.Utils()
    if not tmp_utils.prepare_folder_structure():
      default_logging.append_to_log_file(logger, "Preparing folder structure failed!", logging.FATAL)
      return False
    if not tmp_utils.copy_pdb_files_to_wsl2(self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER]):
      default_logging.append_to_log_file(logger, "Copying pdb files to WSL2 failed!", logging.FATAL)
      return False
    # </editor-fold>
    tmp_number_of_mols = len(os.listdir(constants.Paths.SCRATCH_DIR)) - 1  # -1 due to results dir
    i = 1
    for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_DIR, "*.pdb"):
      if not self.run_ligpargen_command(pathlib.Path(tmp_file)):
        tmp_msg = f"LigParGen conversion of {pathlib.Path(tmp_file).name} failed!"
        default_logging.append_to_log_file(logger, f"LigParGen conversion of {tmp_file} failed!", logging.ERROR)
      else:
        tmp_msg = f"LigParGen conversion of {pathlib.Path(tmp_file).name} finished."
      self._sender_socket.send_json(
        json.dumps({
          "msg": tmp_msg,
          "finished_mols": (i, tmp_number_of_mols),
          "status": "in-progress"
        })
      )
      i += 1
    # <editor-fold desc="Post-processing">
    if not tmp_utils.filter_results(self.job_input_data[constants.JobInputDataKeys.RESULT_FILE_TYPES]):
      return False
    for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_RESULTS_DIR, "*.tinker.*"):
      tmp_path: pathlib.Path = pathlib.Path(tmp_file)
      if tmp_path.suffix == ".xyz":
        post_processing.post_process_tinker_xyz_file(tmp_path)
        os.rename(tmp_path, tmp_file.replace(".tinker.xyz", ".xyz"))
      elif tmp_path.suffix == ".key":
        os.rename(tmp_path, tmp_file.replace(".tinker.key", ".key"))
      else:
        print(f"In {tmp_path} exists no valid tinker file extension!")
        return False
    if "apbs.pqr" in self.job_input_data[constants.JobInputDataKeys.RESULT_FILE_TYPES]:
      for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_DIR, "*.pqr"):
        shutil.copy(pathlib.Path(tmp_file), constants.Paths.SCRATCH_RESULTS_DIR)
    for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_RESULTS_DIR, "*.*"):
      subprocess.run(["unix2dos", tmp_file])
    # </editor-fold>
    # try:
    #   tmp_utils.copy_files_to_windows(constants.Paths.SCRATCH_RESULTS_DIR, self.job_input_data[constants.JobInputDataKeys.OUTPUT_FOLDER])
    # except Exception as e:
    #   default_logging.append_to_log_file(logger, f"An error occurred while copying results: {e}", logging.ERROR)
    #   return False
    return True

  def run_ligpargen_command(self, a_file: pathlib.Path) -> bool:
    try:
      subprocess.run(
        ["bash", str(constants.Paths.LIGPARGEN_BATCH_FILEPATH),
         "-i", str(a_file),
         "-n", str(a_file).replace(a_file.suffix, ""),
         "-c", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOLECULE_CHARGE]),
         "-o", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOL_OPT_ITER]),
         "-cgen", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_CHARGE_MODEL])],
        cwd=str(constants.Paths.SCRATCH_DIR),  # The cwd needs to be set to ensure that the temporarily files of ligpargen are stored there!
        timeout=50
      )
      return True
    except Exception as e:
      print(e)  # TODO: Add logger message here
      return False

  def send_finished_signal(self):
    print("Sending ...")
    self._sender_socket.send_json(
      json.dumps({
        "msg": "Finished LigParGen job.",
        "finished_mols": (0, 1),
        "status": "finished"
      })
    )
