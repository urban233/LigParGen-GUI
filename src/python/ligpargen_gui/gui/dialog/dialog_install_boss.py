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
from ligpargen_gui.model.util import exception, safeguard
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
    self.txt_browser_description = QtWidgets.QTextBrowser()
    tmp_html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LigParGen Requirements</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }
            h2 {
                color: #5e4dcd;
            }
            p {
                margin-bottom: 15px;
            }
            .email {
                color: #0077cc;
                text-decoration: none;
            }
            .email:hover {
                text-decoration: underline;
            }
            .highlight {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h2>LigParGen Software Requirements</h2>
        <p>
          To run <span class="highlight">LigParGen</span>, the <span class="highlight">BOSS (Biochemical and Organic Simulation System)</span> software is a mandatory requirement.
          <span class="highlight">LigParGen</span> depends on <span class="highlight">BOSS</span> for generating OPLS-AA/CM1A(-LBCC) and related parameters, which are crucial for molecular simulations.
          <span class="highlight">BOSS</span> handles tasks such as calculating atomic charges and defining molecular force fields, which are then converted by <span class="highlight">LigParGen</span> into formats suitable for various simulation platforms.
        </p>
        <p><span class="highlight">LigParGen</span> and the <span class="highlight">BOSS</span> software were both developed by the <span class="highlight">William L. Jorgensen Lab at Yale University</span>.</p>
        <p>For academic use, you can send an email directly to Prof. Jorgensen at 
            <span class="highlight">william.jorgensen@yale.edu</span> to acquire <span class="highlight">BOSS 5.0</span>.</p>
        <p>The <span class="highlight">LigParGenGUI</span> software is a front-end to the <span class="highlight">LigParGen</span> Python package.</p>
        <h4>More information</h4>
        <dl>
          <dd><span class="highlight">BOSS</span>: https://zarbi.chem.yale.edu/software.html</dd>
          <dd><span class="highlight">LigParGen</span>: https://github.com/Isra3l/ligpargen</dd>
          <dd><span class="highlight">LigParGenGUI</span>: https://github.com/urban233/ligpargen_gui</dd>
        </dl>
    </body>
    </html>

    """
    self.txt_browser_description.setHtml(tmp_html_content)
    self.lbl = QtWidgets.QLabel("Choose location of Boss tar.gz")
    self.main_layout.addWidget(self.txt_browser_description)
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
    self.resize(500, 600)
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
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(event is not None)
    # </editor-fold>
    event.accept()
    self.dialogClosed.emit()
