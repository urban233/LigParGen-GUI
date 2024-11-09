import logging

from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from ligpargen_gui.gui.base_classes import base_dialog
from ligpargen_gui.gui.custom_widgets import custom_label
from ligpargen_gui.gui.dialog.forms.auto import auto_dialog_compare
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import styles_utils, icons
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class DialogInstallBoss(base_dialog.BaseDialog):
  """Install boss dialog."""

  # <editor-fold desc="Class attributes">
  dialogClosed = QtCore.pyqtSignal()
  """A signal indicating that the dialog is closed."""
  # </editor-fold>

  def __init__(self, a_parent=None) -> None:
    """Constructor."""
    super().__init__(parent=a_parent)
    self.main_layout = QtWidgets.QVBoxLayout()

    # <editor-fold desc="Description label">
    self.lbl = QtWidgets.QLabel("Choose location of Boss tar.gz")
    self.main_layout.addWidget(self.lbl)
    # </editor-fold>
    # <editor-fold desc="Path input">
    input_layout = QtWidgets.QHBoxLayout()
    self.txt_boss_tar_gz_path = QtWidgets.QLineEdit()
    self.btn_boss_tar_gz_path = QtWidgets.QPushButton("...")
    input_layout.addWidget(self.txt_boss_tar_gz_path)
    input_layout.addWidget(self.btn_boss_tar_gz_path)
    self.main_layout.addLayout(input_layout)
    # </editor-fold>
    # <editor-fold desc="Confirmation buttons">
    confirmation_layout = QtWidgets.QHBoxLayout()
    self.btn_ok = QtWidgets.QPushButton("OK")
    self.btn_cancel = QtWidgets.QPushButton("Cancel")
    confirmation_layout.addStretch()
    confirmation_layout.addWidget(self.btn_ok)
    confirmation_layout.addWidget(self.btn_cancel)
    self.main_layout.addLayout(confirmation_layout)
    # </editor-fold>

    self.lbl_error_message = custom_label.ErrorMessageLabel(self)

    self.setLayout(self.main_layout)
    self.setup_ui()
    self.resize(500, 100)
    self.setWindowModality(Qt.WindowModality.WindowModal)

  def setup_ui(self) -> None:
    """Sets up the initial ui."""
    icons.set_icon(self.btn_boss_tar_gz_path, model_definitions.IconsEnum.OPEN)
    self.btn_boss_tar_gz_path.setStyleSheet(
      """
      QPushButton {
          background-color: rgba(220, 219, 227, 0.01);
          border: none;
          border-radius: 4px;
          min-width: 36px;
          max-width: 36px;
          min-height: 36px;
          max-height: 36px;
      }
      QPushButton::hover {
          background-color: rgba(220, 219, 227, 0.5);
          border: none;
          min-width: 40px;
          max-width: 40px;
          min-height: 40px;
          max-height: 40px;
      }
      """
    )
    self.btn_ok.setStyleSheet(
      """
      QPushButton {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }

    QPushButton:disabled {
        background-color: #fff;
        color: #B0B0B0;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }

    QPushButton::pressed {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 2px;
        border-radius: 4px;
        border-color: #367AF6;
        padding: 0px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }
      """
    )
    self.btn_cancel.setStyleSheet(
      """
      QPushButton {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }

    QPushButton:disabled {
        background-color: #fff;
        color: #B0B0B0;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }

    QPushButton::pressed {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 2px;
        border-radius: 4px;
        border-color: #367AF6;
        padding: 0px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }
      """
    )
    styles_utils.set_stylesheet(self)
    self.setWindowTitle("Install BOSS Software")
    self.setWindowFlags(
      self.windowFlags() & ~QtCore.Qt.WindowType.WindowContextHelpButtonHint
    )

  def closeEvent(self, event) -> None:
    """Closes the dialog (with the closeEvent) and emits the 'dialogClosed' signal.

    Args:
      event: The close event.

    Raises:
      exception.NoneValueError: If `event` is None.

    """
    # <editor-fold desc="Checks">
    if event is None:
      default_logging.append_to_log_file(logger, "event is None.", logging.ERROR)
      raise exception.NoneValueError("event is None.")
    # </editor-fold>
    event.accept()
    self.dialogClosed.emit()
