import logging
from typing import Callable, Optional
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QPixmap
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import icons
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class DropDownButton(QtWidgets.QPushButton):
  """Represents a dropdown like button."""

  # <editor-fold desc="Class attributes">
  button_clicked = QtCore.pyqtSignal(tuple)
  """A signal used to indicate that the button was clicked."""
  # </editor-fold>

  def __init__(self, a_button_text: str, a_menu: QtWidgets.QMenu) -> None:
    """Constructor

    Args:
      a_project_name: The name of the project
      a_date_modified: The date the project was last modified
      a_callable: The function to use after the button was clicked.

    Raises:
      exception.NoneValueError: If any of the arguments are None.
      exception.IllegalArgumentError: If `a_button_text` is an empty string.

    Notes:
      IMPORTANT: If the button is clicked the `a_callable` function will
      receive a tuple containing the project name and the date modified.
    """
    # <editor-fold desc="Checks">
    if a_button_text is None:
      default_logging.append_to_log_file(logger, "a_button_text is None.", logging.ERROR)
      raise exception.NoneValueError("a_button_text is None.")
    if a_button_text == "":
      default_logging.append_to_log_file(logger, "a_button_text is an empty string.", logging.ERROR)
      raise exception.IllegalArgumentError("a_button_text is an empty string.")
    if a_menu is None:
      default_logging.append_to_log_file(logger, "a_menu is None.", logging.ERROR)
      raise exception.NoneValueError("a_menu is None.")
    # </editor-fold>
    super().__init__()
    self.menu = a_menu
    self.setText(a_button_text)
    self.setStyleSheet(
      """
      QPushButton {
          background-color: #f5f5f5;
          color: black;
          font-family: "Segoe UI";
          font-size: 12px;
          border: 1px solid #d1d1d1;
          border-radius: 4px;
          padding: 3px;
          padding-left: 7px;
          text-align: left;
      }
      QPushButton::hover {
          background-color: rgba(220, 219, 227, 0.5);
          /*border: none;*/
      }
      QPushButton:disabled {
          background-color: #f5f5f5;
          color: #B0B0B0;
          font-family: "Segoe UI";
          font-size: 12px;
          border: solid;
          border-width: 1px;
          border-radius: 4px;
          border-color: #DCDCDC;
          padding: 3px;
          padding-left: 7px;
          text-align: left;
      }

      QPushButton::pressed {
          background: #d6d6d6;
          color: black;
          font-family: "Segoe UI";
          font-size: 12px;
          /*border-color: #367AF6;*/
      }
      """
    )
    # Set up the main layout directly on the button
    self._layout = QtWidgets.QHBoxLayout(self)
    self._layout.setContentsMargins(0, 0, 0, 0)
    self._layout.setSpacing(0)
    # Set the button to have no default padding
    self.setContentsMargins(0, 0, 0, 0)
    self.icon_label = QtWidgets.QLabel(self)
    icon_pixmap = QPixmap(str(icons.ICON_PATHS["KEYBOARD_ARROW_DOWN_GREY"]))
    self.icon_label.setPixmap(icon_pixmap.scaled(32, 32, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
    self._layout.addStretch(1)
    self._layout.addWidget(self.icon_label)
    # Ensure the layout size is updated
    self.setLayout(self._layout)
    self.setFixedWidth(100)
    self.clicked.connect(self._show_menu)

  def _show_menu(self) -> None:
    """Shows the menu beneath the button."""
    pos = self.mapToGlobal(self.rect().bottomLeft())
    pos.setY(pos.y() + 3)
    self.menu.exec(pos)

  @staticmethod
  def update_button_color(a_drop_down_button: "DropDownButton", a_check_state: bool) -> None:
    """Update the button font color based on checked actions.

    Args:
      a_drop_down_button: The button that should be colored.
      a_check_state: The check state of the QAction that is part of the QMenu which is displayed under the button.

    Raises:
      exception.NoneValueError: If any of the arguments are None.
    """
    # <editor-fold desc="Checks">
    if a_drop_down_button is None:
      default_logging.append_to_log_file(logger, "a_drop_down_button is None.", logging.ERROR)
      raise exception.NoneValueError("a_drop_down_button is None.")
    if a_check_state is None:
      default_logging.append_to_log_file(logger, "a_check_state is None.", logging.ERROR)
      raise exception.NoneValueError("a_check_state is None.")
    # </editor-fold>
    any_checked = any(action.isChecked() for action in a_drop_down_button.menu.actions())
    if any_checked:
      a_drop_down_button.setStyleSheet(
        """
        QPushButton {
            background-color: #f5f5f5;
            color: #367AF6;  /* Change to red if an action is checked */
            font-family: "Segoe UI";
            font-size: 12px;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 3px;
            padding-left: 7px;
            text-align: left;
        }
        QPushButton::hover {
            background-color: rgba(220, 219, 227, 0.5);
        }
        QPushButton:disabled {
            background-color: #f5f5f5;
            color: #B0B0B0;
        }
        """
      )
    else:
      a_drop_down_button.setStyleSheet(
        """
        QPushButton {
            background-color: #f5f5f5;
            color: black;
            font-family: "Segoe UI";
            font-size: 12px;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 3px;
            padding-left: 7px;
            text-align: left;
        }
        QPushButton::hover {
            background-color: rgba(220, 219, 227, 0.5);
        }
        QPushButton:disabled {
            background-color: #f5f5f5;
            color: #B0B0B0;
        }
        QPushButton::pressed {
            background: #d6d6d6;
            color: black;
        }
        """
      )


class PersistentQMenu(QtWidgets.QMenu):
  """Represents a QMenu that keeps open, after a click on any QAction."""

  def __init__(self, parent=None) -> None:
    """Constructor.

    Args:
      parent: The parent widget.
    """
    super().__init__(parent)

  def mouseReleaseEvent(self, event) -> None:
    """Reimplements the method to prevent closing on action click.

    Args:
      event: An event that is sent if the mouse is released.

    Raises:
      exception.NoneValueError: If `event` is None.
    """
    # <editor-fold desc="Checks">
    if event is None:
      default_logging.append_to_log_file(logger, "event is None.", logging.ERROR)
      raise exception.NoneValueError("event is None.")
    # </editor-fold>
    action = self.actionAt(event.pos())
    if action and action.isCheckable():
      # Toggle the action's checked state
      action.setChecked(not action.isChecked())
      # Prevent the menu from closing
      return
    super().mouseReleaseEvent(event)
