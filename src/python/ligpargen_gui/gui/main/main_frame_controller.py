import logging
import pathlib
import subprocess

from PyQt6 import QtWebEngineWidgets, QtCore
from tea.concurrent import task_result, action, task_manager, task_scheduler
from ligpargen_gui.gui.control import compare_controller, status_bar_manager, job_progress_controller
from ligpargen_gui.gui.custom_widgets import custom_label
from ligpargen_gui.gui.dialog import dialog_compare, dialog_job_progress, custom_message_box
from ligpargen_gui.gui.main import main_frame
from ligpargen_gui.gui.util import gui_util, validator
from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.data_classes import ligpargen_options
from ligpargen_gui.model.jobs import ligpargen_job_input
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.qmodel import job_progress_model
from ligpargen_gui.model.util import exception, compare, post_processing
from ligpargen_gui.model.windows import client

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class MainFrameController:
  """Controller class for MainFrame."""

  def __init__(self, a_main_frame: "main_frame.MainFrame") -> None:
    """Constructor.

    Args:
      a_main_frame: The main frame.

    Raises:
      exception.NoneValueError: If `a_main_frame` is None.
    """
    # <editor-fold desc="Checks">
    if a_main_frame is None:
      default_logging.append_to_log_file(logger, "a_main_frame is None.", logging.ERROR)
      raise exception.NoneValueError("a_main_frame is None.")
    # </editor-fold>
    self.main_frame: "main_frame.MainFrame" = a_main_frame
    self.basic_controllers: dict = {
      "Compare": compare_controller.CompareController(dialog_compare.DialogCompare()),
      "JobProgress": job_progress_controller.JobProgressController(dialog_job_progress.DialogJobProgress())
    }
    self.status_bar_manager = status_bar_manager.StatusBarManager(self.main_frame)
    # <editor-fold desc="Tasks">
    self.task_manager = task_manager.TaskManager()
    self.task_scheduler = task_scheduler.TaskScheduler()
    # </editor-fold>
    self.job_progress_model = job_progress_model.JobProgressModel()
    self.connect_all_signals()
    self.update_main_frame_gui()
    self.status_bar_manager.show_temporary_message("Hi there from the status bar!")

  def schedule_tool_task_result_object(
          self,
          a_task_result: tuple[bool, task_result.TaskResult]
  ) -> None:
    """Receives the task result object of the tool and schedules it.

    Args:
      a_task_result: The task result object of the 'create project' tool

    Raises:
      exception.NoneValueError: If `a_task_result` is None.
    """
    # <editor-fold desc="Checks">
    if a_task_result is None:
      default_logging.append_to_log_file(logger, "a_task_result is None.", logging.ERROR)
      raise exception.NoneValueError("a_task_result is None.")
    # </editor-fold>
    if a_task_result[0]:
      self.task_manager.append_task_result(a_task_result[1])
      self.task_scheduler.schedule(a_task_result[1])

  def connect_all_signals(self) -> None:
    """Connects all signals with their slot functions."""
    self.basic_controllers["Compare"].component_task.connect(self.schedule_tool_task_result_object)
    self.main_frame.compare_action.triggered.connect(self.compare_file)
    self.main_frame.exit_action.triggered.connect(self.main_frame.close)
    self.main_frame.txt_structure_input.textChanged.connect(self.__slot_check_structure_path_input)
    self.main_frame.btn_structure_input.clicked.connect(self.__slot_choose_structure_input_path_from_filesystem)
    self.main_frame.txt_output_directory.textChanged.connect(self.__slot_check_output_directory_path)
    self.main_frame.btn_output_directory.clicked.connect(self.__slot_choose_result_path_from_filesystem)
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

  def update_main_frame_gui(self) -> None:
    """Updates the entire gui of the main frame."""
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

  def start_server(self) -> None:
    subprocess.Popen(["wsl", "-d", "alma9LigParGen0205", "-u", "alma_ligpargen", "/home/alma_ligpargen/ligpargen_gui/wsl2/start_server.sh"])

  # <editor-fold desc="Structure input">
  def __slot_choose_structure_input_path_from_filesystem(self) -> None:
    """Chooses a structure input folder path from the filesystem."""
    default_logging.append_to_log_file(
      logger, "'Choose structure input folder from filesystem' button was clicked."
    )
    _, tmp_path = gui_util.open_choose_folder_q_dialog(
      self.main_frame,
      self.main_frame.lbl_structure_input_status,
      self.main_frame.txt_structure_input,
      "Open structure folder"
    )
    self.main_frame.txt_structure_input.setText(tmp_path)
    self.update_main_frame_gui()

  def __slot_check_structure_path_input(self, the_entered_text: str):
    """Checks in real time if the entered path is valid or not.

    Args:
      the_entered_text: The entered path to be checked.

    Raises:
      exception.NoneValueError: If `the_entered_text` is None.
    """
    # <editor-fold desc="Checks">
    if the_entered_text is None:
      default_logging.append_to_log_file(logger, "the_entered_text is None.", logging.ERROR)
      raise exception.NoneValueError("the_entered_text is None.")
    # </editor-fold>
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
    self.update_main_frame_gui()

  # </editor-fold>

  # <editor-fold desc="Output directory">
  def __slot_choose_result_path_from_filesystem(self) -> None:
    """Chooses a results folder path from the filesystem."""
    default_logging.append_to_log_file(
      logger, "'Choose results folder from filesystem' button was clicked."
    )
    _, tmp_path = gui_util.open_choose_folder_q_dialog(
      self.main_frame,
      self.main_frame.lbl_output_directory_status,
      self.main_frame.txt_output_directory,
      "Open results folder"
    )
    self.main_frame.txt_output_directory.setText(tmp_path)
    self.update_main_frame_gui()

  def __slot_check_output_directory_path(self, the_entered_text: str):
    """Checks in real time if the entered path is valid or not.

    Args:
      the_entered_text: The entered path to be checked.

    Raises:
      exception.NoneValueError: If `the_entered_text` is None.
    """
    # <editor-fold desc="Checks">
    if the_entered_text is None:
      default_logging.append_to_log_file(logger, "the_entered_text is None.", logging.ERROR)
      raise exception.NoneValueError("the_entered_text is None.")
    # </editor-fold>"""
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
    self.update_main_frame_gui()
  # </editor-fold>

  # <editor-fold desc="Start job">
  def start_ligpargen_job(self):
    """Starts the ligpargen conversion job."""
    self.job_progress_model = job_progress_model.JobProgressModel()
    self.job_progress_model.create_root_node()
    self.basic_controllers["JobProgress"].set_job_progress_model(self.job_progress_model)
    tmp_job_input = ligpargen_job_input.LigParGenJobInput(
      pathlib.Path(self.main_frame.txt_structure_input.text()),
      pathlib.Path(self.main_frame.txt_output_directory.text()),
      ligpargen_options.LigParGenOptions(
        int(self.main_frame.cbox_mol_optimization_iter.currentText()),
        self.main_frame.cbox_charge_model.currentText(),
        int(self.main_frame.cbox_molecule_charge.currentText())
      ),
      self.main_frame.get_toggled_result_types()
    )
    self.job_progress_model.add_job_progress_message("Starting LigParGen job ...")
    self.basic_controllers["JobProgress"].get_dialog().show()
    self.job_progress_model.add_job_progress_message("Finished LigParGen job!")
    tmp_job_failed_msg_box = custom_message_box.CustomMessageBoxOk(
      "LigParGen job failed!\nPlease consult the log file to get more information.",
      "Job",
      custom_message_box.CustomMessageBoxIcons.DANGEROUS.value,
    )
    tmp_job_failed_msg_box.exec()
    # self.start_server()
    # tmp_client = client.Client()
    # tmp_client.send_job_input(tmp_job_input.serialize())
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
    """Compares the given files with WinMerge in an async manner."""
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
      print(e)
      return False,

  def __await_compare_files(self, value):
    """Awaits the compare files async method and shows the results.

    Args:
      value: a custom result tuple object

    Raises:
      exception.NoneValueError: If `value` is None.
    """
    # <editor-fold desc="Checks">
    if value is None:
      self.main_frame.ui.statusbar.showMessage("The result value is None!")  # TODO: Needs to be replaced by a statusbar manager like in PySSA
      # default_logging.append_to_log_file(logger, "The result value is None!", logging.ERROR)
      return
    if value[1][0] is False:
      self.main_frame.ui.statusbar.showMessage("Compare failed.")  # TODO: Needs to be replaced by a statusbar manager like in PySSA
      # default_logging.append_to_log_file(logger, "Creating project failed!", logging.ERROR)
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
