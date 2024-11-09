import logging
import threading
from typing import Union

from PyQt6 import QtWidgets, QtCore
from ligpargen_gui.model.util import exception
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
    exception.NoneValueError: If any of the arguments are None.
    exception.IllegalArgumentError: If `a_q_file_dialog_caption` is an empty string.
  """
  # <editor-fold desc="Checks">
  if not is_main_thread():
    raise exception.NotMainThreadError()
  if a_parent is None:
    default_logging.append_to_log_file(logger, "a_parent is None.", logging.ERROR)
    raise exception.NoneValueError("a_parent is None.")
  if a_line_edit is None:
    default_logging.append_to_log_file(logger, "a_line_edit is None.", logging.ERROR)
    raise exception.NoneValueError("a_line_edit is None.")
  if a_q_file_dialog_caption is None:
    default_logging.append_to_log_file(logger, "a_q_file_dialog_caption is None.", logging.ERROR)
    raise exception.NoneValueError("a_q_file_dialog_caption is None.")
  if a_q_file_dialog_caption == "":
    default_logging.append_to_log_file(logger, "a_q_file_dialog_caption is an empty string.", logging.ERROR)
    raise exception.IllegalArgumentError("a_q_file_dialog_caption is an empty string.")
  # </editor-fold>
  try:
    file_name = QtWidgets.QFileDialog.getExistingDirectory(
      a_parent,
      a_q_file_dialog_caption,
      QtCore.QDir.homePath(),
    )
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

  Raises:
    exception.NotMainThreadError: If function is called not from the main thread.
    exception.NoneValueError: If any of the arguments are None.
    exception.IllegalArgumentError: If `a_q_file_dialog_caption` is an empty string.
  """
  # <editor-fold desc="Checks">
  if not is_main_thread():
    raise exception.NotMainThreadError()
  if a_parent is None:
    default_logging.append_to_log_file(logger, "a_parent is None.", logging.ERROR)
    raise exception.NoneValueError("a_parent is None.")
  if a_line_edit is None:
    default_logging.append_to_log_file(logger, "a_line_edit is None.", logging.ERROR)
    raise exception.NoneValueError("a_line_edit is None.")
  if a_q_file_dialog_caption is None:
    default_logging.append_to_log_file(logger, "a_q_file_dialog_caption is None.", logging.ERROR)
    raise exception.NoneValueError("a_q_file_dialog_caption is None.")
  if a_q_file_dialog_caption == "":
    default_logging.append_to_log_file(logger, "a_q_file_dialog_caption is an empty string.", logging.ERROR)
    raise exception.IllegalArgumentError("a_q_file_dialog_caption is an empty string.")
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
