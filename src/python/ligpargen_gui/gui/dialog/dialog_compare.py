from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6.QtCore import Qt

from ligpargen_gui.gui.base_classes import base_dialog
from ligpargen_gui.gui.dialog.forms.auto import auto_dialog_compare
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import styles_utils, icons


class DialogCompare(base_dialog.BaseDialog):
  """Compare dialog"""

  dialogClosed = QtCore.pyqtSignal()
  """A signal indicating that the dialog is closed."""

  def __init__(self) -> None:
    """Constructor."""
    super().__init__()
    self.ui = auto_dialog_compare.Ui_Dialog()
    self.ui.setupUi(self)
    self.setup_ui()
    self.resize(650, 370)
    self.ui.btn_cancel.clicked.connect(self.close)
    self.setWindowModality(Qt.WindowModality.WindowModal)

  def setup_ui(self) -> None:
    """Sets up the initial ui."""
    self.ui.cbox_simulation_software.addItems([".tinker"])
    self.ui.cbox_simulation_software.setFixedWidth(80)
    self.ui.cbox_file_extension.addItems(["key", "xyz"])
    self.ui.cbox_file_extension.setFixedWidth(80)

    self.ui.lbl_reference_path_status.setStyleSheet("""color: #ba1a1a; font-size: 11px;""")
    self.ui.lbl_to_compare_path_status.setStyleSheet("""color: #ba1a1a; font-size: 11px;""")
    self.ui.lbl_report_path_status.setStyleSheet("""color: #ba1a1a; font-size: 11px;""")
    icons.set_icon(self.ui.btn_reference_path, model_definitions.IconsEnum.OPEN)
    self.ui.btn_reference_path.setStyleSheet(
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
    icons.set_icon(self.ui.btn_to_compare_path, model_definitions.IconsEnum.OPEN)
    self.ui.btn_to_compare_path.setStyleSheet(
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
    icons.set_icon(self.ui.btn_report_path, model_definitions.IconsEnum.OPEN)
    self.ui.btn_report_path.setStyleSheet(
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
    self.ui.btn_compare.setStyleSheet(
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
    styles_utils.set_stylesheet(self)
    self.setWindowTitle("Define Comparison")
    self.setWindowFlags(
      self.windowFlags() & ~QtCore.Qt.WindowType.WindowContextHelpButtonHint
    )

  def show_help(self):
    # This method is called when the help button is clicked
    QtWidgets.QMessageBox.information(self, 'Help', 'This is the help message.')

  def closeEvent(self, event) -> None:
    """Closes the dialog (with the closeEvent) and emits the 'dialogClosed' signal."""
    event.accept()
    self.dialogClosed.emit()
