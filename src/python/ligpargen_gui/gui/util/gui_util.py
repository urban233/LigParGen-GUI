import logging
import threading
from typing import Union

from PyQt6 import QtWidgets, QtCore
from ligpargen_gui.model.util import exception, safeguard
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


def is_main_thread() -> bool:
  """Check if the current thread is the main thread.

  Returns:
      The boolean True if the current thread is the main thread, False otherwise.
  """
  if threading.current_thread() == threading.main_thread():
    logger.info("Running in main thread.")
    return True
  logger.info("Running in separate thread.")
  return False


def open_choose_folder_q_dialog(
        a_parent: Union[QtWidgets.QDialog, QtWidgets.QMainWindow],
        a_line_edit: QtWidgets.QLineEdit,
        a_q_file_dialog_caption: str
) -> tuple[bool, str]:
  """Opens a choose folder dialog.

  Args:
    a_parent: Either a QDialog or a QMainWindow.
    a_line_edit: The line edit.
    a_q_file_dialog_caption: The caption of the QFileDialog.

  Raises:
    exception.NotMainThreadError: If function is called not from the main thread.

  Returns:
    A tuple containing the boolean True (or False if an exception was caught) if the dialog is opened and the filepath as string
  """
  # <editor-fold desc="Checks">
  if not is_main_thread():
    raise exception.NotMainThreadError()
  safeguard.CHECK(a_parent is not None)
  safeguard.CHECK(a_line_edit is not None)
  safeguard.CHECK(a_q_file_dialog_caption is not None)
  safeguard.CHECK(a_q_file_dialog_caption != "")
  # </editor-fold>
  try:
    file_name = QtWidgets.QFileDialog.getExistingDirectory(
      a_parent,
      a_q_file_dialog_caption,
      QtCore.QDir.homePath(),
    )
    # TODO: This needs to be better handled!
    if file_name == "":
      # a_status_label.setText("No folder has been selected.")
      pass
    else:
      #a_line_edit.setText()  # The QFileDialog returns the path with forward slashes
      # a_status_label.setText("")
      pass
    return True, str(file_name.replace("/", "\\"))
  except Exception as e:
    default_logging.append_to_log_file(logger, str(e), logging.ERROR)
    return False, ""


def open_choose_file_q_dialog(
        a_parent: Union[QtWidgets.QDialog, QtWidgets.QMainWindow],
        a_line_edit: QtWidgets.QLineEdit,
        a_q_file_dialog_caption: str,
        a_file_extension_filter: str = ""
) -> tuple[bool, str]:
  """Opens a choose file dialog.

  Args:
    a_parent: Either a QDialog or a QMainWindow.
    a_line_edit: The line edit.
    a_q_file_dialog_caption: The caption of the QFileDialog.
    a_file_extension_filter: The extension to filter for.

  Raises:
    exception.NotMainThreadError: If function is called not from the main thread.

  Returns:
    A tuple containing the boolean True (or False if an exception was caught) if the dialog is opened and the filepath as string
  """
  # <editor-fold desc="Checks">
  if not is_main_thread():
    raise exception.NotMainThreadError()
  safeguard.CHECK(a_parent is not None)
  safeguard.CHECK(a_line_edit is not None)
  safeguard.CHECK(a_q_file_dialog_caption is not None)
  safeguard.CHECK(a_q_file_dialog_caption != "")
  safeguard.CHECK(a_file_extension_filter is not None)
  # </editor-fold>
  try:
    file_name = QtWidgets.QFileDialog.getOpenFileName(
      a_parent,
      a_q_file_dialog_caption,
      QtCore.QDir.homePath(),
      a_file_extension_filter
    )
    if file_name == ("", ""):
      return True, ""
    return True, str(file_name[0].replace("/", "\\"))
  except Exception as e:
    default_logging.append_to_log_file(logger, str(e), logging.ERROR)
    return False, ""
