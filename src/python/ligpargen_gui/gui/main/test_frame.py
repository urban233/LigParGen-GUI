from PyQt6 import QtCore, QtGui, QtWidgets
from ligpargen_gui.gui.main.forms.auto import auto_test_frame


class TestFrame(QtWidgets.QMainWindow):
  """Test frame class."""

  dialogClosed = QtCore.pyqtSignal(tuple)
  """A signal indicating that the dialog is closed."""

  def __init__(self) -> None:
    """Constructor."""
    super().__init__()
    # build ui object
    self.ui = auto_test_frame.Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.btn_test.clicked.connect(self.placeholder)

  def placeholder(self) -> None:
    """This method functions as dummy and can be substituted by a 'real' method."""
    print("Hello there. - Obi-Wan")
