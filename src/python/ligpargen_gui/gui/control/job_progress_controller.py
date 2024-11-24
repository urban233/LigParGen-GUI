import logging
from typing import TYPE_CHECKING
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from ligpargen_gui.gui.base_classes import base_controller
from ligpargen_gui.gui.util import gui_util
from ligpargen_gui.model.util import exception, safeguard
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"

if TYPE_CHECKING:
  from ligpargen_gui.gui.dialog import dialog_job_progress


class JobProgressController(base_controller.BaseController):
  """Controller for the compare dialog."""

  # <editor-fold desc="Class attributes">
  component_task = QtCore.pyqtSignal(tuple)
  """Custom signal to transfer a TaskResult object with the actual work"""
  # </editor-fold>

  def __init__(self, a_dialog: "dialog_job_progress.DialogJobProgress") -> None:
    """Constructor.
    
    Args:
      a_dialog: A dialog instance to be managed by the controller
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_dialog is not None)
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
    self.restore_ui()
    self.job_progress_model = None
    self.connect_all_signals()

  def connect_all_signals(self) -> None:
    """Connects all signals with their appropriate slot methods."""
    self._dialog.dialogClosed.connect(self.set_dialog_close_as_canceled)
    self._dialog.ui.btn_cancel.clicked.connect(self.close_dialog)
    self._dialog.ui.btn_ok.clicked.connect(self.close_dialog)

  def get_dialog(self) -> QtWidgets.QDialog:
    """Gets the dialog of the controller."""
    return self._dialog
  
  def restore_ui(self) -> None:
    """Restores the UI to default values."""
    self._dialog.setup_ui()

  def set_dialog_close_as_canceled(self) -> None:
    """Sets the was_canceled flag to true."""
    self.was_canceled = True
    self.restore_ui()

  def set_job_progress_model(self, a_job_progress_model) -> None:
    """Sets the job progress model to update the list view with new messages.

    Args:
      a_job_progress_model: The model to manage the job progress messages.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_job_progress_model is not None)
    # </editor-fold>
    self.job_progress_model = a_job_progress_model
    self._dialog.ui.list_view_progress.setModel(self.job_progress_model)

  def set_progress_bar_value(self, a_progress_bar_value: int) -> None:
    """Sets the value of the progress bar.

    Args:
      a_progress_bar_value: The value to set the progress bar to.
    """
    safeguard.CHECK(0 <= a_progress_bar_value <= 100)
    self._dialog.ui.prog_bar.setValue(a_progress_bar_value)

  def close_dialog(self) -> None:
    """Closes the dialog and restores the ui."""
    self._dialog.close()
    self.restore_ui()
