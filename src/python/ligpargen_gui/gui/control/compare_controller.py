import logging
from typing import TYPE_CHECKING
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from ligpargen_gui.gui.base_classes import base_controller
from ligpargen_gui.gui.util import gui_util
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"

if TYPE_CHECKING:
  from ligpargen_gui.gui.dialog import dialog_compare


class CompareController(base_controller.BaseController):
  """Controller for the compare dialog."""

  # <editor-fold desc="Class attributes">
  component_task = QtCore.pyqtSignal(tuple)
  """Custom signal to transfer a TaskResult object with the actual work"""
  # </editor-fold>

  def __init__(self, a_dialog: "dialog_compare.DialogCompare") -> None:
    """Constructor.
    
    Args:
      a_dialog: a dialog instance to be managed by the controller

    Raises:
      exception.NoneValueError: If `a_dialog` is None.
    """
    # <editor-fold desc="Checks">
    if a_dialog is None:
      default_logging.append_to_log_file(logger, "a_dialog is None.", logging.ERROR)
      raise exception.NoneValueError("a_dialog is None.")
    # </editor-fold>
    super().__init__()
    # <editor-fold desc="Instance attributes">
    self._dialog: "dialog_compare.DialogCompare" = a_dialog
    """The dialog that the controller should work with."""
    self.was_canceled: bool = False
    """Flag to indicate whether the dialog was cancelled."""
    self.reference_path: str = ""
    """The path to the reference folder."""
    self.to_compare_path: str = ""
    """The path to the compared folder."""
    self.report_path: str = ""
    """The path where the reports should be saved."""
    self.simulation_software: str = ""
    """The simulation software that is used by the user."""
    self.file_extension: str = ""
    """The file extension that should be compared."""
    # </editor-fold>
    self.connect_all_signals()

  def connect_all_signals(self):
    """Connects all signals with their appropriate slot methods."""
    self._dialog.dialogClosed.connect(self.set_dialog_close_as_canceled)
    self._dialog.ui.btn_reference_path.clicked.connect(self.__slot_choose_reference_path_from_filesystem)
    self._dialog.ui.btn_to_compare_path.clicked.connect(self.__slot_choose_to_compare_path_from_filesystem)
    self._dialog.ui.btn_report_path.clicked.connect(self.__slot_choose_report_path_from_filesystem)
    self._dialog.ui.btn_cancel.clicked.connect(self._dialog.close)
    self._dialog.ui.btn_compare.clicked.connect(self.__slot_compare)

  def get_dialog(self) -> QtWidgets.QDialog:
    """Gets the dialog of the controller."""
    return self._dialog
  
  def restore_ui(self) -> None:
    """Restores the UI to default values."""
    self._dialog.setup_ui()

  def set_dialog_close_as_canceled(self) -> None:
    """Sets the was_canceled flag to true."""
    self.was_canceled = True

  def __slot_choose_reference_path_from_filesystem(self) -> None:
    """Chooses a reference folder path from the filesystem."""
    default_logging.append_to_log_file(
      logger, "'Choose reference folder from filesystem' button was clicked."
    )
    gui_util.open_choose_folder_q_dialog(
      self._dialog,
      self._dialog.ui.lbl_reference_path_status,
      self._dialog.ui.txt_reference_path,
      "Open reference path"
    )

  def __slot_choose_to_compare_path_from_filesystem(self) -> None:
    """Chooses a reference folder path from the filesystem."""
    default_logging.append_to_log_file(
      logger, "'Choose to compare folder from filesystem' button was clicked."
    )
    gui_util.open_choose_folder_q_dialog(
      self._dialog,
      self._dialog.ui.lbl_to_compare_path_status,
      self._dialog.ui.txt_to_compare_path,
      "Open to compare path"
    )

  def __slot_choose_report_path_from_filesystem(self) -> None:
    """Chooses a report folder path from the filesystem."""
    default_logging.append_to_log_file(
      logger, "'Choose report folder from filesystem' button was clicked."
    )
    gui_util.open_choose_folder_q_dialog(
      self._dialog,
      self._dialog.ui.lbl_report_path_status,
      self._dialog.ui.txt_report_path,
      "Open report path"
    )

  def __slot_compare(self) -> None:
    """Slot method for the compare project button."""
    self.reference_path = self._dialog.ui.txt_reference_path.text()
    self.to_compare_path = self._dialog.ui.txt_to_compare_path.text()
    self.report_path = self._dialog.ui.txt_report_path.text()
    self.simulation_software = self._dialog.ui.cbox_file_extension.currentText()
    self.file_extension = self._dialog.ui.cbox_simulation_software.currentText()
    self._dialog.close()  # This triggers the close event
    self.was_canceled = False
