"""Module for the status bar manager."""
import logging

from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets

from ligpargen_gui.gui.custom_widgets import custom_label
from ligpargen_gui.gui.preference import gui_definitions
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import exception, safeguard
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class StatusBarManager:
  """A class to manage the statusbar style and messages."""

  def __init__(self, the_main_view: QtWidgets.QMainWindow) -> None:
    """Constructor.

    Args:
      the_main_view (QMainWindow): The main view of the application.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(the_main_view is not None)
    # </editor-fold>
    self._view = the_main_view
    self._update_signal = None

    self._progress_bar = QtWidgets.QProgressBar()
    self._permanent_message = custom_label.PermanentMessageLabel()

    # Create a button and make it look like a hyperlink
    self.lbl_current_version = QtWidgets.QLabel(f"Version {model_definitions.ModelDefinitions.VERSION_NUMBER.replace('v', '')}")
    self.btn_new_version = QtWidgets.QPushButton("Update")
    self.btn_new_version.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.btn_new_version.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: #0078d7;
            text-decoration: underline;
            border: none;
        }
        QPushButton:hover {
            color: #0056a3;
        }
    """)

    self._menu_task = QtWidgets.QMenu()
    self._is_menu_open = False
    self._abort_action = QtGui.QAction("Abort Job")
    self._menu_task.addAction(self._abort_action)

    self._view.statusBar().addPermanentWidget(self._progress_bar)
    self._view.statusBar().addPermanentWidget(self._permanent_message)
    self._view.statusBar().addPermanentWidget(self.lbl_current_version)
    self._view.statusBar().addPermanentWidget(self.btn_new_version)
    self._progress_bar.hide()
    self.lbl_current_version.hide()
    self.btn_new_version.hide()
    self.temp_message_timer = QtCore.QTimer()

  # <editor-fold desc="Util methods">
  # <editor-fold desc="Methods for styling the status bar">
  def _style_status_bar_for_normal_message(self) -> None:
    """Sets custom style sheet for a normal message."""
    self._view.statusBar().setStyleSheet(
        """
            QStatusBar {
                background-color: #F2F2F2;
                border-style: solid;
                border-width: 2px;
                border-radius: 4px;
                border-color: #DCDBE3;
            }
        """
    )

  def _style_status_bar_for_long_running_task_message(self) -> None:
    """Sets custom style sheet for a long-running message."""
    self._view.statusBar().setStyleSheet(
        """
            QStatusBar {
                background-color: #ff9000;
                border-style: solid;
                border-width: 2px;
                border-radius: 4px;
                border-color: #5b5b5b;
            }
        """
    )

  def _style_status_bar_for_error_message(self) -> None:
    """Sets custom style sheet for an error message."""
    self._view.statusBar().setStyleSheet(
        """
            QStatusBar {
                background-color: #ff9000;
                border-style: solid;
                border-width: 2px;
                border-radius: 4px;
                border-color: #5b5b5b;
            }
        """
    )

  # </editor-fold>
  def _setup_status_bar_message_timer(
      self, running_task: bool = False, the_long_running_task_message: str = ""
  ) -> None:
    """Connects the timer to reset the status bar to the long-running task message.

    Args:
      running_task (bool): Flag for indicating if a long-running task is currently running.
      the_long_running_task_message (str): Message to be displayed when a long-running task is running.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(running_task is not None)
    safeguard.CHECK(the_long_running_task_message is not None)
    # </editor-fold>
    if self.temp_message_timer:
      self.temp_message_timer.stop()  # Stop previous timer if exists
    self.temp_message_timer.setSingleShot(True)
    if running_task:
      self.temp_message_timer.timeout.connect(
          lambda a_long_running_task_message=the_long_running_task_message: self._switch_to_long_running_task_message(
              a_long_running_task_message
          )
      )
    else:
      self.temp_message_timer.timeout.connect(self._restore_status_bar)
    self.temp_message_timer.start(
        5000
    )  # Display temporary message for 5 seconds

  def _switch_to_long_running_task_message(
      self, a_long_running_task_message: str
  ) -> None:
    """Shows a long-running task message as a permanent message.

    Args:
      a_long_running_task_message: Message to set as permanent message.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_long_running_task_message is not None)
    # </editor-fold>
    self.show_permanent_message(a_long_running_task_message)

  def _restore_status_bar(self) -> None:
    """Restores the statusbar."""
    self._style_status_bar_for_normal_message()
    self._view.statusBar().showMessage("")
  # </editor-fold>

  # <editor-fold desc="Public methods">
  def show_permanent_message(self, a_message: str) -> None:
    """Shows a permanent message in the statusbar.

    Args:
      a_message: A string representing the message that will be displayed as a permanent message.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_message is not None)
    # </editor-fold>
    self._permanent_message.setText(a_message)

  def show_error_message(
      self, a_message: str, overwrite_permanent_message: bool = True
  ) -> None:
    """Shows an error message in the statusbar.

    Args:
      a_message (str): The error message to be displayed.
      overwrite_permanent_message (bool, optional): Flag indicating whether to overwrite the permanent message. Defaults to True.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_message is not None)
    safeguard.CHECK(overwrite_permanent_message is not None)
    # </editor-fold>
    self._style_status_bar_for_error_message()
    self._view.statusBar().showMessage("")
    if overwrite_permanent_message is True:
      self._permanent_message.show()
      self._permanent_message.setText(a_message)
    else:
      self._view.statusBar().showMessage(a_message, 999999)

  def show_temporary_message(
      self,
      a_temporary_message: str,
      a_with_timeout_flag: bool = True,
      a_timeout: int = gui_definitions.GuiDefinitions.STATUS_MESSAGE_TIMEOUT,
  ) -> None:
    """Shows a temporary message in the statusbar.

    Args:
      a_temporary_message (str): The message to be displayed temporarily in the status bar.
      a_with_timeout_flag (bool): Optional parameter that specifies whether the message should be displayed for a limited time. Defaults to True.
      a_timeout (int): Optional parameter that specifies the amount of time (in milliseconds) the message should be displayed if a_with_timeout_flag is set to True. Defaults to the value of constants.STATUS_MESSAGE_TIMEOUT.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_temporary_message is not None)
    safeguard.CHECK(a_with_timeout_flag is not None)
    safeguard.CHECK(a_timeout is not None)
    # </editor-fold>
    self._style_status_bar_for_normal_message()
    self._permanent_message.setText("")
    if a_with_timeout_flag:
      self._view.statusBar().showMessage(a_temporary_message, a_timeout)
    else:
      self._view.statusBar().showMessage(a_temporary_message, 999999)

  def update_progress_bar(self, a_message_value_tuple: tuple) -> None:
    """Updates the progress bar with the given message and value.

    Args:
      a_message_value_tuple (tuple): A tuple containing the message and value to be displayed on the progress bar. The message should be a string, and the value should be an integer between 0 and 100 (inclusive).
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_message_value_tuple is not None)
    tmp_message, tmp_value = a_message_value_tuple
    safeguard.CHECK(tmp_value < 0 or tmp_value > 100)
    # </editor-fold>
    self._progress_bar.show()
    self._progress_bar.setFormat(f"{tmp_value}%")
    self._progress_bar.setValue(tmp_value)
    self._permanent_message.show()
    self._permanent_message.setText(tmp_message)

  def hide_progress_bar(self) -> None:
    """Hides the progress bar and reset the permanent message."""
    self._progress_bar.hide()
    self._permanent_message.hide()
    self._permanent_message.setText("")

  def set_update_version(self, a_version) -> None:
    """Sets the update version in the statusbar.

    Args:
      a_version: A string representation of the version to set
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_version is not None)
    # </editor-fold>
    self.lbl_current_version.setText(f"Version {a_version}")

  # </editor-fold>
