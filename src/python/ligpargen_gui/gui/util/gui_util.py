import logging
import threading
from typing import Union

from PyQt6 import QtWidgets, QtCore
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)


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
        a_status_label: QtWidgets.QLabel,
        a_line_edit: QtWidgets.QLineEdit,
        a_dialog_caption: str
) -> bool:
  """Opens a choose folder dialog."""
  try:
    file_name = QtWidgets.QFileDialog.getExistingDirectory(
      a_parent,
      a_dialog_caption,
      QtCore.QDir.homePath(),
    )
    if file_name == "":
      a_status_label.setText("No folder has been selected.")
    else:
      # display path in text box
      a_line_edit.setText(str(file_name.replace("/", "\\")))
      a_status_label.setText("")
    return True
  except Exception as e:
    default_logging.append_to_log_file(logger, str(e), logging.ERROR)
    return False
