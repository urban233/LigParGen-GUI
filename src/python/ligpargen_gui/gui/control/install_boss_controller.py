import logging
from typing import TYPE_CHECKING, Callable
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from ligpargen_gui.gui.base_classes import base_controller
from ligpargen_gui.gui.util import gui_util, validator
from ligpargen_gui.model.util import exception, safeguard
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
    self.boss_is_installed: bool = False
    """Flag to indicate whether the boss software is installed."""
    # </editor-fold>
    self._dialog.txt_boss_tar_gz_path.setEnabled(False)
    self._dialog.btn_ok.setEnabled(False)
    self.connect_all_signals()

  def connect_all_signals(self):
    """Connects all signals with their appropriate slot methods."""
    self._dialog.dialogClosed.connect(self.close_complete_app)
    self._dialog.btn_cancel.clicked.connect(self.close_complete_app)
    self._dialog.btn_ok.clicked.connect(self._dialog.close)
    self._dialog.btn_boss_tar_gz_path.clicked.connect(self.__slot_choose_boss_tar_gz_path_from_filesystem)

  def get_dialog(self) -> QtWidgets.QDialog:
    """Gets the dialog of the controller."""
    return self._dialog
  
  def restore_ui(self) -> None:
    """Restores the UI to default values."""
    self._dialog.setup_ui()

  def set_dialog_close_as_canceled(self) -> None:
    """Sets the was_canceled flag to true."""
    self.was_canceled = True

  def set_slot_method_for_ok_button(self, a_callable: Callable) -> None:
    """Sets a custom function as the slot method for the ok button.

    Args:
      a_callable: Function to connect with the clicked signal of the OK button.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_callable is not None)
    # </editor-fold>
    self._dialog.btn_ok.clicked.disconnect()
    self._dialog.btn_ok.clicked.connect(a_callable)

  def close_complete_app(self) -> None:
    """Closes the entire app."""
    if self.boss_is_installed:
      self.get_dialog().close()
    else:
      exit(0)

  def disable_all_input_widgets(self) -> None:
    """Disables all input widgets."""
    self._dialog.txt_boss_tar_gz_path.setEnabled(False)
    self._dialog.btn_boss_tar_gz_path.setEnabled(False)
    self._dialog.btn_ok.setEnabled(False)
    self._dialog.btn_cancel.setEnabled(False)

  def enable_all_input_widgets(self) -> None:
    """Enables all input widgets."""
    self._dialog.txt_boss_tar_gz_path.clear()
    self._dialog.txt_boss_tar_gz_path.setEnabled(False)
    self._dialog.btn_boss_tar_gz_path.setEnabled(True)
    self._dialog.btn_ok.setEnabled(False)
    self._dialog.btn_cancel.setEnabled(True)

  def __slot_choose_boss_tar_gz_path_from_filesystem(self) -> None:
    """Chooses the boss.tar.gz file from the filesystem."""
    default_logging.append_to_log_file(
      logger, "'Choose boss.tar.gz file from the filesystem' button was clicked."
    )
    _, tmp_path = gui_util.open_choose_file_q_dialog(
      self._dialog,
      self._dialog.txt_boss_tar_gz_path,
      "Choose boss.tar.gz file",
      "*.tar.gz"
    )
    if tmp_path == "":
      if self._dialog.txt_boss_tar_gz_path.text() == "":
        self._dialog.btn_ok.setEnabled(False)
      else:
        self._dialog.btn_ok.setEnabled(True)
    else:
      self._dialog.btn_ok.setEnabled(True)
      self._dialog.txt_boss_tar_gz_path.setText(tmp_path)
