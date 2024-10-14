import logging
import pathlib

from tea.concurrent import task_result, action, task_manager, task_scheduler

from media_forge.gui.control import create_storage_space_controller
from media_forge.gui.dialog import dialog_create_storage_space, dialog_storage_variables
from media_forge.gui.main import main_frame
from media_forge.model.central_objects import storage_space
from media_forge.model.database import databases_manager, database_handler
from media_forge.model.preference import model_definitions
from media_forge.model.pymmm_logging import default_logging
from media_forge.model.qmodel import storage_space_model
from media_forge.model.util import exception

logger = default_logging.setup_logger(__file__)


class MainFrameController:
  """Controller class for MainFrame"""

  def __init__(self, a_main_frame: "main_frame.MainFrame") -> None:
    """Constructor.

    Args:
      a_main_frame: The main frame.

    Raises:
      exception.NoneValueError: If `a_main_frame` is None.
    """
    # <editor-fold desc="Checks">
    if a_main_frame is None:
      #default_logging.append_to_log_file(logger, "a_main_frame is None.", logging.ERROR)
      raise exception.NoneValueError("a_main_frame is None.")
    # </editor-fold>
    self.main_frame: "main_frame.MainFrame" = a_main_frame
    self.databases_manager = databases_manager.DatabasesManager()
    self.basic_controllers: dict = {
      "New": create_storage_space_controller.CreateStorageSpaceController(
        dialog_create_storage_space.DialogCreateStorageSpace())
    }
    # <editor-fold desc="Tasks">
    self.task_manager = task_manager.TaskManager()
    self.task_scheduler = task_scheduler.TaskScheduler()
    # </editor-fold>
    self.storage_space = None
    self.storage_space_model: "storage_space_model.StorageSpaceModel" = storage_space_model.StorageSpaceModel.from_workspace_path(
      model_definitions.ModelDefinitions.DEFAULT_WORKSPACE_PATH, self.async_open_storage_space
    )
    self.main_frame.fill_open_project_scroll_area(
      self.storage_space_model, self.__slot_open_storage_space
    )
    self.main_frame.fill_home_project_scroll_area(
      self.storage_space_model, self.__slot_open_storage_space
    )
    self.connect_all_signals()

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
      #default_logging.append_to_log_file(logger, "a_task_result is None.", logging.ERROR)
      raise exception.NoneValueError("a_task_result is None.")
    # </editor-fold>
    if a_task_result[0]:
      self.task_manager.append_task_result(a_task_result[1])
      self.task_scheduler.schedule(a_task_result[1])

  def connect_all_signals(self):
    """Connects all signals with their slot functions."""
    self.main_frame.ribbon_bar.currentChanged.connect(self._switch_to_storage_space_page)
    self.main_frame.ui.btn_project_page_back.clicked.connect(self._switch_to_main_page)
    self.main_frame.ribbon_bar.connect_all_signals(
      {
        self.main_frame.ribbon_bar.running_action: ("triggered", self.open_running_jobs_side_panel),
        self.main_frame.ribbon_bar.completed_action: ("triggered", self.open_completed_jobs_side_panel),
        self.main_frame.ribbon_bar.tidal_action: ("triggered", self.open_tidal_download_job_side_panel),
        self.main_frame.ribbon_bar.edit_storage_variable_action: ("triggered", self.__slot_open_storage_variables)
      }
    )
    self.main_frame.side_panel_search_tidal.panelClosed.connect(self.main_frame.side_panel_stacked_widget.hide)
    self.main_frame.side_panel_search_tidal.panelOpened.connect(self.main_frame.side_panel_stacked_widget.show)
    self.main_frame.side_panel_running_jobs.panelClosed.connect(self.main_frame.side_panel_stacked_widget.hide)
    self.main_frame.side_panel_running_jobs.panelOpened.connect(self.main_frame.side_panel_stacked_widget.show)
    self.main_frame.side_panel_completed_jobs.panelClosed.connect(self.main_frame.side_panel_stacked_widget.hide)
    self.main_frame.side_panel_completed_jobs.panelOpened.connect(self.main_frame.side_panel_stacked_widget.show)

    self.basic_controllers["New"].component_task.connect(self.schedule_tool_task_result_object)
    self.main_frame.ui.btn_new_blank_project.clicked.connect(self.__slot_open_create_storage_space_dialog)
    self.main_frame.btn_blank_project.clicked.connect(self.__slot_open_create_storage_space_dialog)

  def _switch_to_storage_space_page(self, an_index) -> None:
    """Switches to the storage space page of the main frame stacked widget."""
    if an_index == 0:
      self.main_frame.ui.stackedWidget.setCurrentIndex(1)

  def _switch_to_main_page(self) -> None:
    """Switches to the main page of the main frame stacked widget."""
    self.main_frame.ui.stackedWidget.setCurrentIndex(0)
    self.main_frame.ribbon_bar.setCurrentIndex(1)

  def _switch_side_panel(self, an_index) -> None:
    """Switches the side panel stacked widget.

    Args:
      an_index: The index of stacked widget (location of the side panel)
    """
    if self.main_frame.side_panel_stacked_widget.currentIndex() == an_index and self.main_frame.side_panel_stacked_widget.isVisible():
      self.main_frame.side_panel_stacked_widget.hide()
    else:
      self.main_frame.side_panel_stacked_widget.show()
      self.main_frame.side_panel_stacked_widget.setCurrentIndex(an_index)

  def open_tidal_download_job_side_panel(self) -> None:
    """Opens the tidal download job side panel."""
    self._switch_side_panel(0)

  def open_running_jobs_side_panel(self) -> None:
    """Opens the running jobs side panel."""
    self._switch_side_panel(1)

  def open_completed_jobs_side_panel(self) -> None:
    """Opens the completed jobs side panel."""
    self._switch_side_panel(2)

  def update_main_frame_gui(self) -> None:
    """Updates the entire gui of the main frame."""
    if self.storage_space is None:
      self.main_frame.ui.btn_project_page_back.hide()
    else:
      # A project is open
      self.main_frame.setWindowTitle(f"Media Forge - {self.storage_space.storage_name}")
      self.main_frame.ui.btn_project_page_back.show()
      # <editor-fold desc="Check project name display">
      if self.main_frame.ui.lbl_project_name.text() != "":
        self.main_frame.ui.lbl_project_name.setText(f"Storage space name: {self.storage_space.storage_name}")
      # </editor-fold>

  def close_storage_space(self) -> None:
    """Closes the currently opened storage space."""
    self.storage_space = None
    #self.update_main_frame_gui()

  # <editor-fold desc="New project tab">
  def __slot_open_create_storage_space_dialog(self):
    self.basic_controllers["New"].restore_ui()
    self.basic_controllers["New"].get_dialog().exec()
    tmp_task_result = task_result.TaskResult.from_action(
      action.Action(
        a_target=self.async_create_storage_space
      ),
      self.__await_create_storage_space_task
    )
    if self.basic_controllers["New"].was_canceled is False:
      self.basic_controllers["New"].component_task.emit((True, tmp_task_result))
    else:
      self.basic_controllers["New"].component_task.emit((False, tmp_task_result))

  def async_create_storage_space(self) -> tuple["storage_space.StorageSpace"]:
    """Creates the storage space based on the entered storage name and type."""
    tmp_storage_space = storage_space.StorageSpace(
      self.basic_controllers["New"].entered_storage_space_name,
      self.basic_controllers["New"].chosen_storage_space_type
    )
    return tmp_storage_space,

  def __await_create_storage_space_task(self, value) -> None:
    """Adds the opened storage space to the main frame controller.

    Args:
      value: Result tuple of the finished task
    """
    # <editor-fold desc="Checks">
    if value is None:
      self.main_frame.ui.statusbar.showMessage(
        "The result value is None!")  # TODO: Needs to be replaced by a statusbar manager like in PySSA
      #default_logging.append_to_log_file(logger, "The result value is None!", logging.ERROR)
      return
    if value[1][0] is False:
      self.main_frame.ui.statusbar.showMessage("Creating project failed.")  # TODO: Needs to be replaced by a statusbar manager like in PySSA
      #default_logging.append_to_log_file(logger, "Creating project failed!", logging.ERROR)
      return
    tmp_results = task_result.TaskResult.get_single_action_result(value)
    if tmp_results[0]:
      if self.storage_space is not None:
        self.close_storage_space()
      self.storage_space: "storage_space.StorageSpace" = tmp_results[1][0]
      self.databases_manager.add_handler(
        self.storage_space.storage_name,
        database_handler.DatabaseHandler(
          pathlib.Path(
            f"{model_definitions.ModelDefinitions.DEFAULT_WORKSPACE_PATH}/{self.storage_space.storage_name}.db"
          )
        )
      )
      self.databases_manager.get_handler(self.storage_space.storage_name).is_current_project = True
      tmp_database_work_task = self.databases_manager.get_handler(
        self.storage_space.storage_name).build_new_database_and_change_to_it(
        pathlib.Path(
          f"{model_definitions.ModelDefinitions.DEFAULT_WORKSPACE_PATH}/{self.storage_space.storage_name}.db"
        ),
        self.storage_space.storage_type
      )
      self.task_manager.append_task(tmp_database_work_task)
      self.task_scheduler.schedule_task(tmp_database_work_task)
      #self.build_all_project_related_models()
  # </editor-fold>

  # <editor-fold desc="Open project tab">
  def __slot_open_storage_space(self, a_value: tuple) -> None:
    """Slot method for the open storage space button."""
    tmp_storage_name, tmp_date_modified = a_value
    if self.storage_space is not None:
      self.close_storage_space()
    self.selected_project_name = tmp_storage_name.replace(".json", "")
    tmp_task_result = task_result.TaskResult.from_action(
      action.Action(a_target=self.async_open_storage_space),
      self.__await_component_open_storage_space_task
    )
    self.task_manager.append_task_result(tmp_task_result)
    self.task_scheduler.schedule(tmp_task_result)

  def async_open_storage_space(self) -> tuple["storage_space.StorageSpace"]:
    """Opens the selected storage space"""
    try:
      return storage_space.StorageSpace(self.selected_project_name, model_definitions.StorageSpaceType.MUSIC),  # TODO: StorageSpaceType is at time of writing hard-coded!!!
    except Exception as e:
      default_logging.append_to_log_file(logger, e.__str__(), logging.ERROR)
      raise exception.AsyncOperationFailedError(e.__str__())
    finally:
      default_logging.append_to_log_file(logger, "'async_open_storage_space' method finished.", logging.DEBUG)

  def __await_component_open_storage_space_task(self, value) -> None:
    """Adds the opened project to the main frame controller.

    Args:
      value: Result tuple of the finished task
    """
    # <editor-fold desc="Checks">
    if value is None:
      self.main_frame.ui.statusbar.showMessage(
        "The result value is None!")  # TODO: Needs to be replaced by a statusbar manager like in PySSA
      default_logging.append_to_log_file(logger, "The result value is None!", logging.ERROR)
      return
    if value[1][0] is False:
      self.main_frame.ui.statusbar.showMessage("Opening project failed.")  # TODO: Needs to be replaced by a statusbar manager like in PySSA
      default_logging.append_to_log_file(logger, "Opening project failed!", logging.ERROR)
      return
    # </editor-fold>
    try:
      tmp_results = task_result.TaskResult.get_single_action_result(value)
      if tmp_results[0]:
        if self.storage_space is not None:
          self.databases_manager.get_handler(self.storage_space.storage_name).is_current_project = False
        self.storage_space: "storage_space.StorageSpace" = tmp_results[1][0]
        if self.storage_space.storage_name not in self.databases_manager.handlers.keys():
          """
          Checks if the databases_manager contains already the handler 
          for the given project name.
          The handler could already exist because it may had some inserts 
          to do while not being the active project and therefore still 
          in the databases manager as handler. 
          """
          self.databases_manager.add_handler(
            self.storage_space.storage_name,
            database_handler.DatabaseHandler(
              pathlib.Path(f"{model_definitions.ModelDefinitions.DEFAULT_WORKSPACE_PATH}/{self.storage_space.storage_name}.db")
            )
          )
        self.databases_manager.get_handler(self.storage_space.storage_name).is_current_project = True
        if self.databases_manager.get_handler(self.storage_space.storage_name).is_working is False:
          """
          Checks if the handler is working. 
          If its an old handler it might be not in the do_work loop and 
          needs therefore be restarted.
          Or the handler is already in the do_work loop and without checking
          this, multiple threads for the same handler could coexist 
          which may interfere each other.
          """
          tmp_database_work_task = self.databases_manager.get_handler(self.storage_space.storage_name).create_do_work_task()
          self.task_manager.append_task(tmp_database_work_task)
          self.task_scheduler.schedule_task(tmp_database_work_task)
        tmp_task = task_result.TaskResult.from_action(
          an_action=action.Action(
            a_target=self.__async_fetch_project_from_database,
            args=(
              self.storage_space.storage_name, self.storage_space.storage_type, self.databases_manager.get_handler(self.storage_space.storage_name)
            )
          ),
          an_await_function=self.__await_fetch_project_from_database
        )
        self.task_manager.append_task_result(tmp_task)
        self.task_scheduler.schedule_task_result(tmp_task)
        #self.block_gui(with_wait_cursor=True)
      else:
        self.update_main_frame_gui()
    except Exception as e:
      default_logging.append_to_log_file(
        logger,
        f"An error occurred: {e}",
        logging.ERROR
      )
      #self.status_bar_manager.show_error_message("An error occurred.")

  def __async_fetch_project_from_database(self, a_storage_space_name: str, a_storage_type: "model_definitions.StorageSpaceType", a_database_handler: "database_handler.DatabaseHandler") -> "project.Project":
    """ASYNC method that fetches all data for the project from the database.

    Args:
      a_storage_space_name: The name of the project
      a_database_handler: The database handler of the project to fetch

    Raises:
      exception.NoneValueError: If any of the arguments are None.
      exception.IllegalArgumentError: If `a_project_name` is an empty string.
    """
    # <editor-fold desc="Checks">
    if a_storage_space_name is None:
      default_logging.append_to_log_file(logger, "a_storage_space_name is None.", logging.ERROR)
      raise exception.NoneValueError("a_storage_space_name is None.")
    if a_storage_space_name == "":
      default_logging.append_to_log_file(logger, "a_storage_space_name is an empty string.", logging.ERROR)
      raise exception.IllegalArgumentError("a_storage_space_name is an empty string.")
    if a_database_handler is None:
      default_logging.append_to_log_file(logger, "a_database_handler is None.", logging.ERROR)
      raise exception.NoneValueError("a_database_handler is None.")
    # </editor-fold>
    return a_database_handler.get_complete_storage_space(a_storage_space_name, a_storage_type)

  def __await_fetch_project_from_database(self, a_result: tuple[str, list]) -> None:
    """Finishes up the open project process."""
    try:
      if a_result[0]:
        self.storage_space = task_result.TaskResult.get_single_action_result(a_result)[1]
        #self.build_all_project_related_models()
        self.databases_manager.remove_unused_handlers()  # This must run after a GUI-reorganization method!
    except Exception as e:
      default_logging.append_to_log_file(
        logger,
        f"An error occurred: {e}",
        logging.ERROR
      )
      #self.status_bar_manager.show_error_message("An error occurred.")
    finally:
      self.main_frame.ribbon_bar.setCurrentIndex(1)
      self.update_main_frame_gui()
      #self.stop_wait_cursor()
      #self.unblock_gui()
  # </editor-fold>

  def __slot_open_storage_variables(self):
    self.dialog = dialog_storage_variables.DialogStorageVariables()
    self.dialog.exec()
