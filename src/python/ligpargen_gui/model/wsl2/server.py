import json
import logging
import os.path
import pathlib
import shutil
import subprocess

import zmq
from wsl2 import constants, utils
from wsl2 import post_processing, safeguard
from wsl2 import default_logging, exception

logger = default_logging.setup_logger(__file__)


class Server:
  """Class for communicating the client in Windows."""
  def __init__(self) -> None:
    """Constructor."""
    context = zmq.Context()
    self._recv_socket = context.socket(zmq.PULL)
    self._recv_socket.bind("tcp://127.0.0.1:8033")
    self._sender_socket = context.socket(zmq.PUSH)
    self._sender_socket.bind("tcp://127.0.0.1:8034")
    self.job_input_data: dict = {}

  def listen_for_job_input(self) -> bool:
    """Listens for any new job input.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    try:
      tmp_utils = utils.Utils()
      self.job_input_data: dict = json.loads(self._recv_socket.recv_json())
      if self.job_input_data[constants.JobInputDataKeys.JOB_TYPE] == constants.JobTypes.INSTALL_BOSS:
        self.job_input_data[constants.JobInputDataKeys.BOSS_TAR_GZ_FILEPATH] = tmp_utils.windows_to_wsl_path(self.job_input_data[constants.JobInputDataKeys.BOSS_TAR_GZ_FILEPATH])
      elif self.job_input_data[constants.JobInputDataKeys.JOB_TYPE] == constants.JobTypes.RUN_LIGPARGEN:
        self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER] = tmp_utils.windows_to_wsl_path(self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER])
        self.job_input_data[constants.JobInputDataKeys.OUTPUT_FOLDER] = tmp_utils.windows_to_wsl_path(self.job_input_data[constants.JobInputDataKeys.OUTPUT_FOLDER])
      else:
        default_logging.append_to_log_file(logger, "Unknown job type!", logging.ERROR)
        return False
      return True
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False

  def run_job(self) -> bool:
    """Runs job based on job type.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    try:
      if self.job_input_data[constants.JobInputDataKeys.JOB_TYPE] == constants.JobTypes.INSTALL_BOSS:
        default_logging.append_to_log_file(logger, "Job type: INSTALL BOSS", logging.INFO)
        if not self.run_install_boss_job():
          default_logging.append_to_log_file(logger, "Install BOSS software job failed.", logging.ERROR)
          return False
        else:
          default_logging.append_to_log_file(logger, "Install BOSS software job finished.", logging.INFO)
          return True
      elif self.job_input_data[constants.JobInputDataKeys.JOB_TYPE] == constants.JobTypes.RUN_LIGPARGEN:
        default_logging.append_to_log_file(logger, "Job type: RUN LIGPARGEN", logging.INFO)
        if not self.run_ligpargen_job():
          default_logging.append_to_log_file(logger, "LigParGen job failed.", logging.ERROR)
          return False
        else:
          default_logging.append_to_log_file(logger, "LigParGen job finished.", logging.INFO)
          return True
      else:
        return False
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False

  def run_install_boss_job(self) -> bool:
    """Runs the 'install boss' job.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    try:
      tmp_utils = utils.Utils()
      pathlib.Path("/home/alma_ligpargen/BOSS_FILES").mkdir(exist_ok=True)
      # <editor-fold desc="Copy tar into WSL2">
      self.send_progress("Copy BOSS archive into WSL2 ...", (3, 10))
      if not tmp_utils.run_shell_command(
        ["cp", self.job_input_data[constants.JobInputDataKeys.BOSS_TAR_GZ_FILEPATH], "/home/alma_ligpargen/BOSS_FILES/"]
      ):
        tmp_msg = "Copying the boss.tar.gz into the WSL2 distro failed!"
        default_logging.append_to_log_file(logger, tmp_msg, logging.ERROR)
        self._sender_socket.send_json(
          json.dumps({
            "msg": tmp_msg,
            "finished_mols": (3, 10),
            "status": "in-progress"
          })
        )
        return False
      # </editor-fold>
      # <editor-fold desc="Unpack tar file">
      self.send_progress("Unpack BOSS archive ...", (6, 10))
      if not tmp_utils.run_shell_command(
        ["tar", "-xf", "/home/alma_ligpargen/BOSS_FILES/boss0824.tar.gz", "-C", "/home/alma_ligpargen"]
      ):
        tmp_msg = "Unpacking the boss.tar.gz failed!"
        default_logging.append_to_log_file(logger, tmp_msg, logging.ERROR)
        self._sender_socket.send_json(
          json.dumps({
            "msg": tmp_msg,
            "finished_mols": (6, 10),
            "status": "in-progress"
          })
        )
        return False
      # </editor-fold>
      # <editor-fold desc="Verify boss files">
      self.send_progress("Verify BOSS installation files ...", (7, 10))
      if not tmp_utils.compare_directory_to_snapshot(
              "/home/alma_ligpargen/boss", "/home/alma_ligpargen/ligpargen_gui/wsl2/boss_snapshot.json"
      ):
        tmp_msg = "The given boss directory does not contain all files that it should!"
        default_logging.append_to_log_file(logger, tmp_msg, logging.ERROR)
        self._sender_socket.send_json(
          json.dumps({
            "msg": tmp_msg,
            "finished_mols": (7, 10),
            "status": "in-progress"
          })
        )
        return False
      # </editor-fold>
      # <editor-fold desc="Change ownership to alma_ligpargen">
      if not tmp_utils.run_shell_command(["chown", "-R", "alma_ligpargen:alma_ligpargen", "/home/alma_ligpargen/boss"]):
        tmp_msg = "Changing the ownership of the boss directory failed!"
        default_logging.append_to_log_file(logger, tmp_msg, logging.ERROR)
        self._sender_socket.send_json(
          json.dumps({
            "msg": tmp_msg,
            "finished_mols": (7, 10),
            "status": "in-progress"
          })
        )
        return False
      # </editor-fold>
      return True
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False

  def run_ligpargen_job(self) -> bool:
    """Runs the 'ligpargen' job.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    try:
      # <editor-fold desc="Preparations">
      default_logging.append_to_log_file(logger, "Preparing environment ...", logging.INFO)
      tmp_utils = utils.Utils()
      if not tmp_utils.prepare_folder_structure():
        default_logging.append_to_log_file(logger, "Preparing folder structure failed!", logging.ERROR)
        return False
      if not tmp_utils.copy_input_files_to_wsl2(pathlib.Path(self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER])):
        default_logging.append_to_log_file(logger, "Copying pdb files to WSL2 failed!", logging.ERROR)
        return False
      subprocess.run(["dos2unix", str(constants.Paths.LIGPARGEN_BATCH_FILEPATH)])
      default_logging.append_to_log_file(logger, "Preparing environment finished.", logging.INFO)
      # </editor-fold>
      # <editor-fold desc="Convert SMILES">
      if pathlib.Path(self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER]).is_file():
        tmp_filepath = pathlib.Path(constants.Paths.SCRATCH_DIR / pathlib.Path(self.job_input_data[constants.JobInputDataKeys.INPUT_FOLDER]).name)
        # Open the file in read mode
        with open(str(tmp_filepath), "r") as file:
          # Read all lines and remove the newline characters
          tmp_smiles = [tmp_line.strip() for tmp_line in file.readlines()]
        default_logging.append_to_log_file(logger, f"These are the SMILES: {tmp_smiles}", logging.INFO)
        tmp_number_of_mols = len(tmp_smiles)
        i = 1
        for tmp_smiles_code in tmp_smiles:
          default_logging.append_to_log_file(logger, f"Starting LigParGen conversion of {tmp_smiles_code} ...", logging.INFO)
          if not self.run_ligpargen_command_with_smiles(tmp_smiles_code):
            tmp_msg = f"LigParGen conversion of {tmp_smiles_code} failed!"
            default_logging.append_to_log_file(logger, f"LigParGen conversion of {tmp_smiles_code} failed!", logging.ERROR)
          else:
            tmp_msg = f"LigParGen conversion of {tmp_smiles_code} finished."
            default_logging.append_to_log_file(logger, f"LigParGen conversion of {tmp_smiles_code} finished", logging.INFO)
          self._sender_socket.send_json(
            json.dumps({
              "msg": tmp_msg,
              "finished_mols": (i, tmp_number_of_mols),
              "status": "in-progress"
            })
          )
          i += 1
      # </editor-fold>
      # <editor-fold desc="Convert PDB files">
      else:
        tmp_number_of_mols = len(os.listdir(constants.Paths.SCRATCH_DIR)) - 1  # -1 due to results dir
        i = 1
        for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_DIR, "*.pdb"):
          default_logging.append_to_log_file(logger, f"Starting LigParGen conversion of {tmp_file} ...", logging.INFO)
          if not self.run_ligpargen_command(pathlib.Path(tmp_file)):
            tmp_msg = f"LigParGen conversion of {pathlib.Path(tmp_file).name} failed!"
            default_logging.append_to_log_file(logger, f"LigParGen conversion of {tmp_file} failed!", logging.ERROR)
          else:
            tmp_msg = f"LigParGen conversion of {pathlib.Path(tmp_file).name} finished."
            default_logging.append_to_log_file(logger, f"LigParGen conversion of {tmp_file} finished", logging.INFO)
          self._sender_socket.send_json(
            json.dumps({
              "msg": tmp_msg,
              "finished_mols": (i, tmp_number_of_mols),
              "status": "in-progress"
            })
          )
          i += 1
      # </editor-fold>
      # <editor-fold desc="Post-processing">
      default_logging.append_to_log_file(logger, "Post processing result files ...", logging.INFO)
      if not tmp_utils.filter_results(self.job_input_data[constants.JobInputDataKeys.RESULT_FILE_TYPES]):
        return False
      for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_RESULTS_DIR, "*.tinker.*"):
        tmp_path: pathlib.Path = pathlib.Path(tmp_file)
        # <editor-fold desc="Post-process TINKER .xyz file">
        if tmp_path.suffix == ".xyz":
          if not post_processing.post_process_tinker_xyz_file(tmp_path):
            tmp_msg = f"Could not post-process the file {tmp_path.name}!"
            default_logging.append_to_log_file(logger, tmp_msg, logging.WARNING)
            self._sender_socket.send_json(
              json.dumps({
                "msg": tmp_msg,
                "finished_mols": (i, tmp_number_of_mols),
                "status": "in-progress"
              })
            )
          else:
            os.rename(tmp_path, tmp_file.replace(".tinker.xyz", ".xyz"))
        # </editor-fold>
        elif tmp_path.suffix == ".key":
          os.rename(tmp_path, tmp_file.replace(".tinker.key", ".key"))
        else:
          default_logging.append_to_log_file(logger, f"In {tmp_path} exists no valid tinker file extension!", logging.ERROR)
          return False
      if "apbs.pqr" in self.job_input_data[constants.JobInputDataKeys.RESULT_FILE_TYPES]:
        for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_DIR, "*.pqr"):
          shutil.copy(pathlib.Path(tmp_file), constants.Paths.SCRATCH_RESULTS_DIR)
      for tmp_file in tmp_utils.loop_over_directory_with_wildcard(constants.Paths.SCRATCH_RESULTS_DIR, "*.*"):
        subprocess.run(["unix2dos", tmp_file])
      default_logging.append_to_log_file(logger, "Post processing result files finished.", logging.INFO)
      # </editor-fold>
      return True
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False

  def run_ligpargen_command(self, a_file: pathlib.Path) -> bool:
    """Runs a single ligpargen command for a pdb file.

    Args:
      a_file: The pdb file to convert with ligpargen.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    # <editor-fold desc="Checks">
    safeguard.ENSURE(a_file is not None)
    safeguard.ENSURE(a_file.exists())
    # </editor-fold>
    try:
      tmp_complete_process = subprocess.run(
        ["bash", str(constants.Paths.LIGPARGEN_BATCH_FILEPATH),
         "-i", str(a_file),
         "-n", str(a_file).replace(a_file.suffix, ""),
         "-c", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOLECULE_CHARGE]),
         "-o", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOL_OPT_ITER]),
         "-cgen", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_CHARGE_MODEL])],
        cwd=str(constants.Paths.SCRATCH_DIR),  # The cwd needs to be set to ensure that the temporarily files of ligpargen are stored there!
        timeout=int(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_TIMEOUT]),
        capture_output=True
      )
      default_logging.append_to_log_file(logger, f"The value of the CompletedProcess object of the LigParGen command is: {tmp_complete_process}", logging.DEBUG)
      if tmp_complete_process.returncode != 0:
        default_logging.append_to_log_file(logger, "Error: Usage or syntax error occurred.", logging.ERROR)
        default_logging.append_to_log_file(logger, f"Error output: {tmp_complete_process.stderr.decode()}", logging.ERROR)
        return False
      else:
        return True
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False

  def run_ligpargen_command_with_smiles(self, a_smiles: str) -> bool:
    """Runs a single ligpargen command for an SMILES input.

    Args:
      a_smiles: SMILES string.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    # <editor-fold desc="Checks">
    safeguard.ENSURE(a_smiles is not None)
    safeguard.ENSURE(a_smiles != "")
    # </editor-fold>
    try:
      tmp_complete_process = subprocess.run(
        ["bash", str(constants.Paths.LIGPARGEN_BATCH_FILEPATH),
         "-s", a_smiles,
         "-n", a_smiles,
         "-c", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOLECULE_CHARGE]),
         "-o", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_MOL_OPT_ITER]),
         "-cgen", str(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_CHARGE_MODEL])],
        cwd=str(constants.Paths.SCRATCH_DIR),  # The cwd needs to be set to ensure that the temporarily files of ligpargen are stored there!
        timeout=int(self.job_input_data[constants.JobInputDataKeys.OPTIONS][constants.JobInputDataKeys.OPTIONS_TIMEOUT]),
        capture_output=True
      )
      default_logging.append_to_log_file(logger, f"The value of the CompletedProcess object of the LigParGen command is: {tmp_complete_process}", logging.DEBUG)
      if tmp_complete_process.returncode != 0:
        default_logging.append_to_log_file(logger, "Error: Usage or syntax error occurred.", logging.ERROR)
        default_logging.append_to_log_file(logger, f"Error output: {tmp_complete_process.stderr.decode()}", logging.ERROR)
        return False
      else:
        return True
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False

  def send_finished_signal(self, a_msg: str, has_failed: bool = False) -> bool:
    """Sends the finished signal.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    # <editor-fold desc="Checks">
    safeguard.ENSURE(a_msg is not None)
    safeguard.ENSURE(has_failed is not None)
    # </editor-fold>
    try:
      if has_failed:
        tmp_status = "failed"
      else:
        tmp_status = "finished"
      self._sender_socket.send_json(
        json.dumps({
          "msg": a_msg,
          "finished_mols": (1, -1),  # -1 indicates a finished job
          "status": tmp_status
        })
      )
      return True
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False

  def send_progress(self, a_msg: str, a_progress: tuple) -> bool:
    """Sends a progress report signal.

    Args:
      a_msg: A message that describes the progress.
      a_progress: A tuple containing the finished molecules and total molecules.

    Returns:
      True if the process was successful, Otherwise: False.
    """
    # <editor-fold desc="Checks">
    safeguard.ENSURE(a_msg is not None)
    safeguard.ENSURE(a_progress is not None)
    # </editor-fold>
    try:
      self._sender_socket.send_json(
        json.dumps({
          "msg": a_msg,
          "finished_mols": a_progress,
          "status": "in-progress"
        })
      )
      return True
    except Exception as e:
      default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.ERROR)
      return False
