import logging
from typing import TYPE_CHECKING, Callable
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from ligpargen_gui.gui.base_classes import base_controller
from ligpargen_gui.gui.util import gui_util
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"

if TYPE_CHECKING:
  from ligpargen_gui.gui.dialog import dialog_install_boss


class InstallBossController(base_controller.BaseController):
  """Controller for the 'install boss' dialog."""

  # <editor-fold desc="Class attributes">
  component_task = QtCore.pyqtSignal(tuple)
  """Custom signal to transfer a TaskResult object with the actual work"""
  # </editor-fold>

  def __init__(self, a_dialog: "dialog_install_boss.DialogInstallBoss") -> None:
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
    self.boss_is_installed: bool = False
    """Flag to indicate whether the boss software is installed."""
    # </editor-fold>
    self.connect_all_signals()

  def connect_all_signals(self):
    """Connects all signals with their appropriate slot methods."""
    self._dialog.dialogClosed.connect(self.close_complete_app)
    self._dialog.btn_cancel.clicked.connect(self.close_complete_app)
    self._dialog.btn_ok.clicked.connect(self._dialog.close)

  def get_dialog(self) -> QtWidgets.QDialog:
    """Gets the dialog of the controller."""
    return self._dialog
  
  def restore_ui(self) -> None:
    """Restores the UI to default values."""
    self._dialog.setup_ui()

  def set_dialog_close_as_canceled(self) -> None:
    """Sets the was_canceled flag to true."""
    self.was_canceled = True

  def set_slot_method_for_ok_button(self, a_callable: Callable):
    """Sets a custom function as the slot method for the ok button."""
    self._dialog.btn_ok.clicked.disconnect()
    self._dialog.btn_ok.clicked.connect(a_callable)

  def close_complete_app(self):
    """Closes the entire app."""
    if self.boss_is_installed:
      self.get_dialog().close()
    else:
      exit(0)

  def disable_all_input_widgets(self):
    """Disables all input widgets."""
    self._dialog.txt_boss_tar_gz_path.setEnabled(False)
    self._dialog.btn_boss_tar_gz_path.setEnabled(False)
    self._dialog.btn_ok.setEnabled(False)
    self._dialog.btn_cancel.setEnabled(False)

  def enable_all_input_widgets(self):
    """Enables all input widgets."""
    self._dialog.txt_boss_tar_gz_path.clear()
    self._dialog.txt_boss_tar_gz_path.setEnabled(True)
    self._dialog.btn_boss_tar_gz_path.setEnabled(True)
    self._dialog.btn_ok.setEnabled(False)
    self._dialog.btn_cancel.setEnabled(True)
