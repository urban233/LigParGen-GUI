import logging

from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from ligpargen_gui.gui.base_classes import base_dialog
from ligpargen_gui.gui.dialog.forms.auto import auto_dialog_job_progress
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import styles_utils, icons
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class DialogJobProgress(base_dialog.BaseDialog):
  """Compare dialog."""

  # <editor-fold desc="Class attributes">
  dialogClosed = QtCore.pyqtSignal()
  """A signal indicating that the dialog is closed."""
  # </editor-fold>

  def __init__(self, a_parent) -> None:
    """Constructor."""
    super().__init__(parent=a_parent)
    self.ui = auto_dialog_job_progress.Ui_Dialog()
    self.ui.setupUi(self)
    self.setup_ui()
    self.resize(650, 370)
    self.ui.btn_cancel.clicked.connect(self.close)
    self.setWindowModality(Qt.WindowModality.WindowModal)

  def setup_ui(self) -> None:
    """Sets up the initial ui."""
    self.ui.list_view_progress.setEnabled(False)
    self.ui.prog_bar.setValue(0)
    self.ui.btn_ok.setEnabled(False)
    self.ui.list_view_progress.setStyleSheet("""
      QListView:disabled { color: #2d2f2e; }
    """)
    self.ui.btn_cancel.setStyleSheet(
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
    self.ui.btn_ok.setStyleSheet(
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
    self.setWindowTitle("LigParGen Job Status")
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
