"""Module for the custom label widget."""
from PyQt6 import QtWidgets
from PyQt6 import QtCore

from ligpargen_gui.model.util import safeguard


class PermanentMessageLabel(QtWidgets.QLabel):
  """A custom label widget that can send a signal if the text changes."""

  # <editor-fold desc="Class attributes">
  textChanged = QtCore.pyqtSignal(str)
  """A signal indicating that the text changed."""
  # </editor-fold>

  def __init__(self, parent=None) -> None:  # noqa: ANN001
    """Constructor."""
    super().__init__(parent)

  def setText(self, text) -> None:
    """Overrides the setText method of the QLabel class.

    Args:
      text (str): The text to set.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(text is not None)
    # </editor-fold>
    super().setText(text)
    self.textChanged.emit(text)


class ErrorMessageLabel(QtWidgets.QLabel):
  """A custom label to display an error message above a line edit."""
  def __init__(self, parent=None) -> None:
    # Set up the QLabel for the tooltip-like message
    super().__init__(parent)
    self.setStyleSheet("""
      color: #2d2f2e; 
      background-color: #fff2f3; 
      border: 1px solid #efaab1; 
      padding-top: 3px;
      padding-bottom: 3px;
      padding-left: 6px;
      padding-right: 6px;
    """)
    self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.setGeometry(50, 0, 200, 20)  # Position it above the QLineEdit
    self.hide()  # Hide initially
    # Timer to hide the tooltip after a delay
    self.tooltip_timer = QtCore.QTimer(self)
    self.tooltip_timer.setSingleShot(True)
    self.tooltip_timer.timeout.connect(self.hide)

  def show_message(self, a_position: QtCore.QPoint, a_message):
    """Shows the message.

    Args:
      a_position: A point where the message should be shown.
      a_message: The message to show.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_position is not None)
    safeguard.CHECK(a_message is not None)
    # </editor-fold>
    self.setText(a_message)
    self.adjustSize()  # Adjust the size to fit the message
    #self.move(a_line_edit.geometry().x() + 75, a_line_edit.geometry().y())
    self.move(a_position)
    self.show()
    # Start or restart the timer to hide the tooltip after 2 seconds
    self.tooltip_timer.start(3000)
