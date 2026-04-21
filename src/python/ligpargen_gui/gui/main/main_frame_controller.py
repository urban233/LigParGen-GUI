import json
import logging
import pathlib
import shutil
import subprocess

from PyQt6 import QtWebEngineWidgets, QtCore
from tea.concurrent import task_result, action, task_manager, task_scheduler, task_result_factory
from ligpargen_gui.gui.control import compare_controller, status_bar_manager, job_progress_controller, \
  install_boss_controller
from ligpargen_gui.gui.custom_widgets import custom_label
from ligpargen_gui.gui.dialog import dialog_compare, dialog_job_progress, custom_message_box, dialog_install_boss, \
  dialog_about
from ligpargen_gui.gui.main import main_frame
from ligpargen_gui.gui.util import gui_util, validator
from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.data_classes import ligpargen_options
from ligpargen_gui.model.jobs import ligpargen_job_input, install_boss_job_input
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.qmodel import job_progress_model
from ligpargen_gui.model.util import exception, compare, post_processing, filesystem_util, powershell, url, safeguard
from ligpargen_gui.model.windows import client

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class MainFrameController:
  """Controller class for MainFrame."""

  def __init__(self, a_main_frame: "main_frame.MainFrame") -> None:
    """Constructor.

    Args:
      a_main_frame: The main frame.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_main_frame is not None)
    # </editor-fold>
    self.main_frame: "main_frame.MainFrame" = a_main_frame
    self.basic_controllers: dict = {
      "InstallBoss": install_boss_controller.InstallBossController(dialog_install_boss.DialogInstallBoss(self.main_frame)),
      "Compare": compare_controller.CompareController(dialog_compare.DialogCompare()),
      "JobProgress": job_progress_controller.JobProgressController(dialog_job_progress.DialogJobProgress(self.main_frame))
    }
    self.status_bar_manager = status_bar_manager.StatusBarManager(self.main_frame)
    self.client = client.Client()
    # <editor-fold desc="Tasks">
    self.task_manager = task_manager.TaskManager()
    self.task_scheduler = task_scheduler.TaskScheduler()
    # </editor-fold>
    self.job_progress_model = job_progress_model.JobProgressModel()
    self.connect_all_signals()
    self.update_main_frame_gui()
    if self.check_if_boss_is_installed():
      if self.check_if_update_is_available():
        self.status_bar_manager.btn_new_version.show()
      else:
        self.status_bar_manager.btn_new_version.hide()

  def schedule_tool_task_result_object(
          self,
          a_task_result: tuple[bool, task_result.TaskResult]
  ) -> None:
    """Receives the task result object of the tool and schedules it.

    Args:
      a_task_result: The task result object of the 'create project' tool
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_task_result is not None)
    # </editor-fold>
    try:
      if a_task_result[0]:
        self.task_manager.append_task_result(a_task_result[1])
        self.task_scheduler.schedule(a_task_result[1])
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def connect_all_signals(self) -> None:
    """Connects all signals with their slot functions."""
    self.basic_controllers["Compare"].component_task.connect(self.schedule_tool_task_result_object)
    #self.main_frame.compare_action.triggered.connect(self.compare_file)
    self.main_frame.open_logs_folder_action.triggered.connect(self.__slot_open_logs)
    self.main_frame.clear_all_logs_action.triggered.connect(self.__slot_clear_all_log_files)
    self.main_frame.about_action.triggered.connect(self.__slot_open_about)
    self.main_frame.exit_action.triggered.connect(self.main_frame.close)
    self.main_frame.txt_structure_input.textChanged.connect(self.__slot_check_structure_path_input)
    self.main_frame.btn_structure_input.clicked.connect(self.__slot_choose_structure_input_type)
    self.main_frame.action_structure_input_pdb.triggered.connect(self.__slot_choose_pdb_folder_path_from_filesystem)
    self.main_frame.action_structure_input_smiles.triggered.connect(self.__slot_choose_smiles_text_filepath_from_filesystem)
    self.main_frame.txt_timeout.textChanged.connect(self.__slot_check_timeout_input)
    self.main_frame.txt_output_directory.textChanged.connect(self.__slot_check_output_directory_path)
    self.main_frame.btn_output_directory.clicked.connect(self.__slot_choose_result_path_from_filesystem)
    self.main_frame.tg_select_all.toggleChanged.connect(self.__slot_select_all_result_types)
    # <editor-fold desc="Result file actions">
    self.main_frame.action_apbs_pqr.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_charmm_pdb.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_charmm_prm.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_charmm_rtf.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_desmond_cms.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_gromacs_gro.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_gromacs_itp.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_lammps_lmp.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_openmm_pdb.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_openmm_xml.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_q_lib.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_q_pdb.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_q_prm.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_tinker_xyz.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_tinker_key.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_xplor_param.toggled.connect(self.update_main_frame_gui)
    self.main_frame.action_xplor_top.toggled.connect(self.update_main_frame_gui)
    # </editor-fold>
    self.main_frame.btn_start_job.clicked.connect(self.start_ligpargen_job)
    self.client.progress_signal.connect(self.update_progress_dialog)
    self.status_bar_manager.btn_new_version.clicked.connect(self.update_application)

  def update_main_frame_gui(self) -> None:
    """Updates the entire gui of the main frame."""
    try:
      tmp_structure_input_path = pathlib.Path(self.main_frame.txt_structure_input.text())
      tmp_output_directory_path = pathlib.Path(self.main_frame.txt_output_directory.text())

      # <editor-fold desc="Structure input path is invalid">
      if not tmp_structure_input_path.exists():
        default_logging.append_to_log_file(logger, "Update GUI: Structure input path is invalid", logging.DEBUG)
        self.main_frame.btn_start_job.setEnabled(False)
        self.main_frame.accordion_section_options.setEnabled(False)
        self.main_frame.accordion_section_results.setEnabled(False)
      # </editor-fold>
      # <editor-fold desc="Structure input is empty">
      elif self.main_frame.txt_structure_input.text() == "":
        default_logging.append_to_log_file(logger, "Update GUI: Structure input path is empty", logging.DEBUG)
        self.main_frame.btn_start_job.setEnabled(False)
        self.main_frame.accordion_section_options.setEnabled(False)
        self.main_frame.accordion_section_results.setEnabled(False)
      # </editor-fold>
      # <editor-fold desc="Structure input path is valid">
      else:
        default_logging.append_to_log_file(logger, "Update GUI: Structure input path is valid", logging.DEBUG)
        # <editor-fold desc="Output directory path is invalid">
        if not tmp_output_directory_path.exists():
          default_logging.append_to_log_file(logger, "Update GUI: Output directory path is invalid", logging.DEBUG)
          self.main_frame.accordion_section_options.setEnabled(True)
          self.main_frame.accordion_section_results.setEnabled(True)
          self.main_frame.btn_start_job.setEnabled(False)
        # </editor-fold>
        elif self.main_frame.txt_output_directory.text() == "":
          default_logging.append_to_log_file(logger, "Update GUI: Output directory path is empty", logging.DEBUG)
          self.main_frame.accordion_section_options.setEnabled(True)
          self.main_frame.accordion_section_results.setEnabled(True)
          self.main_frame.btn_start_job.setEnabled(False)
        else:
          default_logging.append_to_log_file(logger, "Update GUI: Output directory path is valid", logging.DEBUG)
          # <editor-fold desc="Output directory path is valid">
          if not self.main_frame.a_result_is_toggled():
            default_logging.append_to_log_file(logger, "Update GUI: No result file is checked", logging.DEBUG)
            self.main_frame.accordion_section_options.setEnabled(True)
            self.main_frame.accordion_section_results.setEnabled(True)
            self.main_frame.btn_start_job.setEnabled(False)
          else:
            default_logging.append_to_log_file(logger, "Update GUI: At least one result file is checked", logging.DEBUG)
            self.main_frame.accordion_section_options.setEnabled(True)
            self.main_frame.accordion_section_results.setEnabled(True)
            self.main_frame.btn_start_job.setEnabled(True)
          # </editor-fold>
      # </editor-fold>
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def update_progress_dialog(self, a_progress_info: tuple) -> None:
    """Updates the progress bar dialog with a new message and progbar value.

    Args:
      a_progress_info: A tuple containing a message and the number of finished molecules.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_progress_info is not None)
    # </editor-fold>
    try:
      tmp_msg, tmp_finished_mols, _ = a_progress_info
      if tmp_finished_mols[1] != -1:  # -1 indicates a finished job
        self.job_progress_model.add_job_progress_message(tmp_msg)
        tmp_progress = (tmp_finished_mols[0]/tmp_finished_mols[1]) * 80
      else:
        tmp_progress = 80
      self.basic_controllers["JobProgress"].set_progress_bar_value(int(tmp_progress))
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def check_if_update_is_available(self) -> bool:
    """Checks if an update is available.

    Returns:
      True if the versions are different and therefore an update is available. Otherwise: False.
    """
    # TODO: This feature needs a complete new implementation due to link sharing
    #   restrictions of Sciebo. This would mean manually looking up if a new version
    #   is available at least for now.
    return False
    if model_definitions.ModelDefinitions.REMOTE_VERSION_FILEPATH.exists():
      model_definitions.ModelDefinitions.REMOTE_VERSION_FILEPATH.unlink()
    if not url.download_file(model_definitions.ModelDefinitions.URL_TO_REMOTE_VERSION, model_definitions.ModelDefinitions.REMOTE_VERSION_FILEPATH):
      self.status_bar_manager.show_temporary_message("Could not check for updates! Please try again later.")
      return False
    try:
      # Open and load the JSON file
      with open(model_definitions.ModelDefinitions.REMOTE_VERSION_FILEPATH, 'r') as file:
        data = json.load(file)
      # Extract the latest version from the versionHistory list
      latest_version = data["versionHistory"][-1]["version"]
      current_version = model_definitions.ModelDefinitions.VERSION_NUMBER.replace("v", "")
      # Check if the latest version matches the target version
      if latest_version == current_version:
        default_logging.append_to_log_file(logger, f"The version {latest_version} matches the target version.", logging.INFO)
        self.status_bar_manager.lbl_current_version.hide()
        self.status_bar_manager.btn_new_version.hide()
        return False
      else:
        default_logging.append_to_log_file(logger, f"The version {latest_version} does NOT match the target version {current_version}.", logging.INFO)
        self.status_bar_manager.lbl_current_version.show()
        self.status_bar_manager.btn_new_version.show()
        self.status_bar_manager.set_update_version(latest_version)
        return True
    except (json.JSONDecodeError, KeyError, IndexError) as e:
      default_logging.append_to_log_file(logger, f"Error parsing the file or accessing version: {e}", logging.ERROR)
      return True
    except FileNotFoundError:
      self.status_bar_manager.show_temporary_message("Could not check for updates! Please try again later.")
      self.status_bar_manager.lbl_current_version.hide()
      self.status_bar_manager.btn_new_version.hide()
      return False

  def check_if_boss_is_installed(self) -> bool:
    """Checks if the BOSS software is installed in the WSL2 and prompts the user if not.

    Returns:
      True if BOSS is installed. Otherwise: False.
    """
    tmp_boss_is_installed = filesystem_util.check_file_exists_in_wsl(
      model_definitions.ModelDefinitions.DISTRO_NAME, "/home/alma_ligpargen/boss/BOSS"
    )
    if not tmp_boss_is_installed:
      self.basic_controllers["InstallBoss"].set_slot_method_for_ok_button(self.open_progress_dialog_for_boss_install)
      self.basic_controllers["InstallBoss"].get_dialog().show()
      return False
    else:
      return True

  def open_progress_dialog_for_boss_install(self) -> None:
    """Opens the job progress dialog for the boss installation."""
    self.basic_controllers["InstallBoss"].disable_all_input_widgets()
    self.job_progress_model = job_progress_model.JobProgressModel()
    self.job_progress_model.create_root_node()
    self.basic_controllers["JobProgress"].set_job_progress_model(self.job_progress_model)
    self.job_progress_model.add_job_progress_message("Installing BOSS software ...")
    tmp_job_input = install_boss_job_input.InstallBossJobInput(
      pathlib.Path(self.basic_controllers["InstallBoss"].get_dialog().txt_boss_tar_gz_path.text())
    )
    self.task_manager.append_task_result(
      task_result_factory.TaskResultFactory.run_task_result(
        a_task_result=task_result.TaskResult.from_action(
          an_action=action.Action(
            a_target=self.async_run_install_boss_job,
            args=(tmp_job_input,),
          ),
          an_await_function=self.__await_install_boss
        ),
        a_task_scheduler=self.task_scheduler
      )
    )
    self.basic_controllers["JobProgress"].get_dialog().setWindowTitle("Install BOSS Status")
    self.basic_controllers["JobProgress"].get_dialog().show()

  def async_run_install_boss_job(self, a_job_input: "install_boss_job_input.InstallBossJobInput") -> None:
    """Installs the boss software with the given tar.gz file.

    Args:
      a_job_input: A job input describing the job to run.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_job_input is not None)
    # </editor-fold>
    self.start_server()
    tmp = a_job_input.serialize(a_job_input.get_obj_as_dict())
    self.client.send_job_input(tmp)
    self.client.check_progress_status()

  def __await_install_boss(self) -> None:
    """Awaits the installation of the boss software."""
    self.shutdown_wsl2_distro()
    if self.client.job_status == "failed":
      self.job_progress_model.add_job_progress_message("Installing BOSS software failed!")
      self.basic_controllers["InstallBoss"].boss_is_installed = False
      self.basic_controllers["JobProgress"].set_progress_bar_value(int(0))
      tmp_job_failed_msg_box = custom_message_box.CustomMessageBoxOk(
        "The installation of the BOSS software failed!",
        "Install BOSS Failed",
        custom_message_box.CustomMessageBoxIcons.ERROR.value,
      )
      tmp_job_failed_msg_box.exec()
      self.basic_controllers["InstallBoss"].enable_all_input_widgets()
      self.basic_controllers["JobProgress"].get_dialog().close()
    elif self.client.job_status == "finished":
      self.job_progress_model.add_job_progress_message("Installing BOSS software finished!")
      self.basic_controllers["InstallBoss"].boss_is_installed = True
      self.basic_controllers["InstallBoss"].get_dialog().close()
      self.basic_controllers["JobProgress"].set_progress_bar_value(int(100))
      tmp_job_failed_msg_box = custom_message_box.CustomMessageBoxOk(
        "The installation of the BOSS software was successful.",
        "Install BOSS Finished",
        custom_message_box.CustomMessageBoxIcons.INFORMATION.value,
      )
      tmp_job_failed_msg_box.exec()
      self.basic_controllers["JobProgress"].get_dialog().ui.btn_cancel.setEnabled(False)
      self.basic_controllers["JobProgress"].get_dialog().ui.btn_ok.setEnabled(True)
    else:
      default_logging.append_to_log_file(logger, f"Unknown job status after job has finished: {self.client.job_status}", logging.WARNING)

  def start_server(self) -> None:
    """Starts the server.py in the WSL2 with a linux shell script."""
    subprocess.Popen(
      [
        "wsl",
        "-d", model_definitions.ModelDefinitions.DISTRO_NAME,
        "-u", "alma_ligpargen", "/home/alma_ligpargen/ligpargen_gui/wsl2/start_server.sh"
      ],
      creationflags=subprocess.CREATE_NO_WINDOW
    )

  def shutdown_wsl2_distro(self) -> None:
    """Shuts down the WSL2 distro."""
    # Clean scratch directory
    subprocess.run(
      [
        "wsl",
        "-d", model_definitions.ModelDefinitions.DISTRO_NAME,
        "-u", "alma_ligpargen",
        "rm", "-r", "/home/alma_ligpargen/ligpargen_gui/scratch"
       ],
      creationflags=subprocess.CREATE_NO_WINDOW
    )
    subprocess.run(
      [
        "wsl",
        "--terminate", model_definitions.ModelDefinitions.DISTRO_NAME
      ],
      creationflags=subprocess.CREATE_NO_WINDOW
    )

  # <editor-fold desc="Help menu methods">
  def __slot_open_about(self) -> None:
    """Opens the About dialog."""
    try:
      tmp_dialog = dialog_about.DialogAbout()
      tmp_dialog.exec()
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def __slot_open_logs(self) -> None:
    """Opens a file explorer with all log files and can open a log file in the default application."""
    try:
      subprocess.run(["explorer.exe", str(model_definitions.ModelDefinitions.DEFAULT_LOG_PATH)])
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def __slot_clear_all_log_files(self) -> None:
    """Clears all log files generated under .pyssa/logs."""
    try:
      tmp_dialog = custom_message_box.CustomMessageBoxYesNo(
        "Are you sure you want to delete all log files?",
        "Clear Log Files",
        custom_message_box.CustomMessageBoxIcons.WARNING.value,
      )
      tmp_dialog.exec()
      if tmp_dialog.response:
        try:
          shutil.rmtree(str(model_definitions.ModelDefinitions.DEFAULT_WINDOWS_LOG_PATH))
        except PermissionError:
          default_logging.append_to_log_file(logger, "The active windows log file was not deleted.", logging.INFO)
        if not model_definitions.ModelDefinitions.DEFAULT_WINDOWS_LOG_PATH.exists():
          model_definitions.ModelDefinitions.DEFAULT_WINDOWS_LOG_PATH.mkdir(parents=True)
        try:
          shutil.rmtree(str(model_definitions.ModelDefinitions.DEFAULT_WSL2_LOG_PATH))
        except PermissionError:
          default_logging.append_to_log_file(logger, "The active wsl2 log file was not deleted.", logging.INFO)
        if not model_definitions.ModelDefinitions.DEFAULT_WSL2_LOG_PATH.exists():
          model_definitions.ModelDefinitions.DEFAULT_WSL2_LOG_PATH.mkdir(parents=True)
        powershell.await_run_wsl_command(
          ["sudo", "rm", "-r", "/home/alma_ligpargen/ligpargen_gui/logs/*"]
        )
        self.status_bar_manager.show_temporary_message("All log files were deleted.")
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")
  # </editor-fold>

  # <editor-fold desc="Structure input">
  def __slot_choose_structure_input_type(self) -> None:
    """Opens a QMenu to choose a structure input type."""
    try:
      pos = self.main_frame.btn_structure_input.mapToGlobal(self.main_frame.btn_structure_input.rect().bottomLeft())
      pos.setY(pos.y() + 3)
      self.main_frame.structure_input_menu.exec(pos)
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def __slot_choose_pdb_folder_path_from_filesystem(self) -> None:
    """Chooses a pdb folder path from the filesystem."""
    try:
      _, tmp_path = gui_util.open_choose_folder_q_dialog(
        self.main_frame,
        self.main_frame.txt_structure_input,
        "Open PDB structure(s) folder"
      )
      if tmp_path != "":
        self.main_frame.txt_structure_input.setText(tmp_path)
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")
    finally:
      self.update_main_frame_gui()

  def __slot_choose_smiles_text_filepath_from_filesystem(self) -> None:
    """Chooses a smiles filepath from the filesystem."""
    try:
      _, tmp_path = gui_util.open_choose_file_q_dialog(
        self.main_frame,
        self.main_frame.txt_structure_input,
        "Open SMILES text file",
        "*.txt"
      )
      if tmp_path != "":
        self.main_frame.txt_structure_input.setText(tmp_path)
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")
    finally:
      self.update_main_frame_gui()

  def __slot_check_structure_path_input(self, the_entered_text: str) -> None:
    """Checks in real time if the entered path is valid or not.

    Args:
      the_entered_text: The entered path to be checked.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(the_entered_text is not None)
    # </editor-fold>
    try:
      tmp_success, tmp_status_text, tmp_stylesheet = validator.validate_path(the_entered_text)
      if tmp_success:
        self.main_frame.lbl_error_message.hide()
      else:
        self.main_frame.lbl_error_message.show_message(
          QtCore.QPoint(
            self.main_frame.txt_structure_input.geometry().x() + 75,
            self.main_frame.txt_structure_input.geometry().y()
          ),
          tmp_status_text
        )
      self.main_frame.txt_structure_input.setStyleSheet(tmp_stylesheet)
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")
      self.update_main_frame_gui()

  # </editor-fold>

  def __slot_check_timeout_input(self, the_entered_text: str) -> None:
    """Checks in real time if the entered timeout is valid or not.

    Args:
      the_entered_text: The entered timeout to be checked.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(the_entered_text is not None)
    # </editor-fold>
    try:
      tmp_success, tmp_status_text = validator.validate_timeout(the_entered_text)
      self.main_frame.txt_timeout.setText(tmp_status_text)
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def __slot_select_all_result_types(self) -> None:
    """Selects all result types."""
    try:
      if self.main_frame.tg_select_all.toggle_button.isChecked():
        self.main_frame.toggle_all_results()
      else:
        self.main_frame.untoggle_all_results()
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")
    finally:
      self.update_main_frame_gui()

  # <editor-fold desc="Output directory">
  def __slot_choose_result_path_from_filesystem(self) -> None:
    """Chooses a results folder path from the filesystem."""
    try:
      _, tmp_path = gui_util.open_choose_folder_q_dialog(
        self.main_frame,
        self.main_frame.txt_output_directory,
        "Open results folder"
      )
      self.main_frame.txt_output_directory.setText(tmp_path)
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")
    finally:
      self.update_main_frame_gui()

  def __slot_check_output_directory_path(self, the_entered_text: str) -> None:
    """Checks in real time if the entered path is valid or not.

    Args:
      the_entered_text: The entered path to be checked.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(the_entered_text is not None)
    # </editor-fold>"""
    try:
      tmp_success, tmp_status_text, tmp_stylesheet = validator.validate_path(the_entered_text)
      if tmp_success:
        self.main_frame.lbl_error_message.hide()
      else:
        pos = self.main_frame.txt_output_directory.mapToGlobal(QtCore.QPoint(0, 0))
        # I could not figure out how to not set the offsets manually
        # (someone is needed that understands the positioning in PyQt6)
        pos.setX(120)
        pos.setY(pos.y() - 251)
        self.main_frame.lbl_error_message.show_message(pos, tmp_status_text)
      self.main_frame.txt_output_directory.setStyleSheet(tmp_stylesheet)
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")
    finally:
      self.update_main_frame_gui()
  # </editor-fold>

  # <editor-fold desc="Start job">
  def start_ligpargen_job(self) -> None:
    """Starts the ligpargen conversion job."""
    try:
      self.job_progress_model = job_progress_model.JobProgressModel()
      self.job_progress_model.create_root_node()
      self.basic_controllers["JobProgress"].set_job_progress_model(self.job_progress_model)
      if self.main_frame.txt_timeout.text() != "":
        tmp_timeout = int(self.main_frame.txt_timeout.text())
      else:
        tmp_timeout = 60
      tmp_job_input = ligpargen_job_input.LigParGenJobInput(
        pathlib.Path(self.main_frame.txt_structure_input.text()),
        pathlib.Path(self.main_frame.txt_output_directory.text()),
        ligpargen_options.LigParGenOptions(
          int(self.main_frame.cbox_mol_optimization_iter.currentText()),
          self.main_frame.cbox_charge_model.currentText(),
          int(self.main_frame.cbox_molecule_charge.currentText()),
          tmp_timeout
        ),
        self.main_frame.get_toggled_result_types()
      )
      self.job_progress_model.add_job_progress_message("Starting LigParGen job ...")
      self.task_manager.append_task_result(
        task_result_factory.TaskResultFactory.run_task_result(
          a_task_result=task_result.TaskResult.from_action(
            an_action=action.Action(
              a_target=self.async_run_ligpargen_job,
              args=(tmp_job_input, ),
            ),
            an_await_function=self.__await_run_ligpargen_job
          ),
          a_task_scheduler=self.task_scheduler
        )
      )
      self.basic_controllers["JobProgress"].get_dialog().setWindowTitle("LigParGen Job Status")
      self.basic_controllers["JobProgress"].get_dialog().show()
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def async_run_ligpargen_job(self, a_job_input: "ligpargen_job_input.LigParGenJobInput") -> None:
    """Runs a ligpargen job asynchronously.

    Args:
      a_job_input: The job input of the job to run.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_job_input is not None)
    # </editor-fold>
    self.start_server()
    self.client.send_job_input(a_job_input.serialize(a_job_input.get_obj_as_dict()))
    self.client.check_progress_status()
    if not self.client.copy_results(a_job_input.output_folder):
      self.client.job_status = "failed"

  def __await_run_ligpargen_job(self) -> None:
    """Awaits the ligpargen job and runs post-job tasks."""
    self.shutdown_wsl2_distro()
    if self.client.job_status == "failed":
      self.job_progress_model.add_job_progress_message("LigParGen job failed!")
      self.basic_controllers["JobProgress"].set_progress_bar_value(int(0))
      tmp_msg_box = custom_message_box.CustomMessageBoxYesNo(
        "LigParGen job failed!\nPlease consult the log file to get more information.\nDo you want to open the log folder now?",
        "Job",
        custom_message_box.CustomMessageBoxIcons.DANGEROUS.value,
      )
      tmp_msg_box.exec()
      if tmp_msg_box.response:
        subprocess.run(["explorer.exe", model_definitions.ModelDefinitions.DEFAULT_WINDOWS_LOG_PATH])  # TODO: Sub with wsl2 log path under Windows!
    elif self.client.job_status == "finished":
      self.job_progress_model.add_job_progress_message("LigParGen job finished!")
      self.basic_controllers["JobProgress"].set_progress_bar_value(int(100))
      tmp_msg_box = custom_message_box.CustomMessageBoxYesNo(
        "The LigParGen job finished.\nDo you want to open the output folder?",
        "Job",
        custom_message_box.CustomMessageBoxIcons.INFORMATION.value,
      )
      tmp_msg_box.exec()
      if tmp_msg_box.response:
        subprocess.run(["explorer.exe", str(pathlib.Path(self.main_frame.txt_output_directory.text()))])
    else:
      default_logging.append_to_log_file(logger, f"Unknown job status after job has finished: {self.client.job_status}", logging.WARNING)
    self.basic_controllers["JobProgress"].get_dialog().ui.btn_cancel.setEnabled(False)
    self.basic_controllers["JobProgress"].get_dialog().ui.btn_ok.setEnabled(True)
  # </editor-fold>

  # <editor-fold desc="Compare files">
  def compare_file(self) -> None:
    """Compares files using WinMerge."""
    # pwd: C:\Users\student\github_repos\LigParGen-GUI
    # TODO: Change hard-coded test paths to variable ones (only for testing purposes)
    self.basic_controllers["Compare"].restore_ui()
    self.basic_controllers["Compare"].get_dialog().ui.txt_reference_path.setText(
      r"C:\Users\student\user_space\projects\ligpargen\LigParGen_Test\web_server_results")
    self.basic_controllers["Compare"].get_dialog().ui.txt_to_compare_path.setText(
      r"C:\Users\student\user_space\projects\ligpargen\LigParGen_Test\local_results\optimization_3")
    self.basic_controllers["Compare"].get_dialog().ui.txt_report_path.setText(
      r"C:\Users\student\github_repos\LigParGen-GUI\test_files")
    self.basic_controllers["Compare"].get_dialog().exec()
    tmp_task_result = task_result.TaskResult.from_action(
      action.Action(
        a_target=self.async_compare_files
      ),
      self.__await_compare_files
    )
    if self.basic_controllers["Compare"].was_canceled is False:
      self.basic_controllers["Compare"].component_task.emit((True, tmp_task_result))
    else:
      self.basic_controllers["Compare"].component_task.emit((False, tmp_task_result))

  def async_compare_files(self) -> tuple[bool]:
    """Compares the given files with WinMerge in an async manner.

    Returns:
      A tuple with only a boolean indicating the success of the method.
    """
    try:
      compare.compare_files(
        pathlib.Path(self.basic_controllers["Compare"].reference_path),
        pathlib.Path(self.basic_controllers["Compare"].to_compare_path),
        pathlib.Path(self.basic_controllers["Compare"].report_path),
        self.basic_controllers["Compare"].simulation_software,
        self.basic_controllers["Compare"].file_extension
      )
      return True,
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      return False,

  def __await_compare_files(self, value) -> None:
    """Awaits the compare files async method and shows the results.

    Args:
      value: a custom result tuple object
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(value is not None)
    if value[1][0] is False:
      self.status_bar_manager.show_error_message("Compare failed.")
      return
    # </editor-fold>
    tmp_results = task_result.TaskResult.get_single_action_result(value)
    if tmp_results[0]:
      self.main_frame.ui.statusbar.showMessage(
        "Compare was successful.")  # TODO: Needs to be replaced by a statusbar manager like in PySSA
      # TODO: Needs to be moved to another place (just for testing purposes!)
      # Create a QWebEngineView to display the HTML content
      self.browser = QtWebEngineWidgets.QWebEngineView()
      # Load the HTML file
      self.browser.setUrl(QtCore.QUrl.fromLocalFile(r"C:\Users\student\github_repos\LigParGen-GUI\test_files\AcCO_key_report.html"))
      self.browser.show()
  # </editor-fold>

  def update_application(self) -> None:
    """Starts the update routine for the application."""
    try:
      tmp_msg_box = custom_message_box.CustomMessageBoxYesNo(
        "There is a new update avaliable. Do you want to update now?",
        "Update",
        custom_message_box.CustomMessageBoxIcons.INFORMATION.value,
      )
      tmp_msg_box.exec()
      if tmp_msg_box.response:
        self.status_bar_manager.show_temporary_message("Downloading update.exe ...", False)
        self.task_manager.append_task_result(
          task_result_factory.TaskResultFactory.run_task_result(
            a_task_result=task_result.TaskResult.from_action(
              an_action=action.Action(
                a_target=self.async_update_application,
                args=(0,),
              ),
              an_await_function=self.__await_update_application
            ),
            a_task_scheduler=self.task_scheduler
          )
        )
        self.main_frame.block_gui()
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      self.status_bar_manager.show_error_message("An error occurred.")

  def async_update_application(self, a_placeholder) -> bool:
    """Starts the update asynchronously.

    Returns:
      A boolean indicating if the download of the update.exe was successful.
    """
    # Get the path to the current user's Downloads folder
    tmp_update_exe_filepath = pathlib.Path.home() / "Downloads" / "update.exe"
    if not url.download_file(model_definitions.ModelDefinitions.URL_TO_UPDATE_SETUP, tmp_update_exe_filepath):
      return False
    else:
      return True

  def __await_update_application(self, result: bool) -> None:
    """Awaits the download of the update setup.

    Args:
      result: A boolean that is True if the update.exe was successfully downloaded.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(result is not None)
    # </editor-fold>
    if result:
      tmp_job_failed_msg_box = custom_message_box.CustomMessageBoxOk(
        "The application will now close and run the update automatically.",
        "Update",
        custom_message_box.CustomMessageBoxIcons.INFORMATION.value,
      )
      tmp_job_failed_msg_box.exec()
      tmp_update_exe_filepath = pathlib.Path.home() / "Downloads" / "update.exe"
      subprocess.Popen([tmp_update_exe_filepath, "/SILENT"])
      exit(0)
    else:
      tmp_job_failed_msg_box = custom_message_box.CustomMessageBoxOk(
        "Downloading the update failed!",
        "Update failed",
        custom_message_box.CustomMessageBoxIcons.ERROR.value,
      )
      tmp_job_failed_msg_box.exec()
