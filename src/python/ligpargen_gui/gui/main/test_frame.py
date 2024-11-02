import subprocess

from PyQt6 import QtCore, QtWidgets
from ligpargen_gui.gui.main.forms.auto import auto_test_frame
from ligpargen_gui.model.preference import model_definitions


class TestFrame(QtWidgets.QMainWindow):
  """Test frame class."""

  # <editor-fold desc="Class attributes">
  dialogClosed = QtCore.pyqtSignal(tuple)
  """A signal indicating that the dialog is closed."""
  # </editor-fold>

  def __init__(self) -> None:
    """Constructor."""
    super().__init__()
    # build ui object
    self.ui = auto_test_frame.Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.btn_test.clicked.connect(self.start_server)

  def start_server(self) -> None:
    subprocess.run(["wsl", "-d", model_definitions.ModelDefinitions.DISTRO_NAME, "-u", "alma_ligpargen", "/home/alma_ligpargen/ligpargen_gui/wsl2/start_server.sh"])
