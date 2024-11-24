"""Module for all custom signals which can be used as arguments either in the main thread or in separate threads."""
import logging
from typing import TYPE_CHECKING
from typing import Callable

from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets
from ligpargen_gui.model.util import exception, safeguard
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)
__docformat__ = "google"


class ProgressSignal(QtCore.QObject):
  """Signal for progress reporting."""

  # <editor-fold desc="Class attributes">
  progress = pyqtSignal(tuple)
  """Signal indicating a progress has been made with the form (message, progress value)."""
  # </editor-fold>

  def emit_signal(self, a_message: str, a_value: int) -> bool:
    """Emits a signal with a message and a value to update the progress.

    Args:
      a_message (str): The message to update the progress.
      a_value (int): The value to update the progress.

    Returns:
      True: Operation successful, False: Otherwise
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_message is not None)
    safeguard.CHECK(a_value is not None)
    safeguard.CHECK(a_value > 0 or a_value < 100)
    # </editor-fold>
    try:
      self.progress.emit((a_message, a_value))
    except Exception as e:
      logger.error(e)
      return False
    else:
      return True


class AbortSignal(QtCore.QObject):
  """Signal to initialize the abort of an operation."""

  # <editor-fold desc="Class attributes">
  abort = pyqtSignal(tuple)
  """Signal indicating to abort an operation with the form (bool, source)."""
  # </editor-fold>

  def emit_signal(self, a_source: Callable) -> bool:
    """Emits the signal.

    Args:
      a_source (Callable): The function or task where the signal is to be emitted.

    Returns:
      True: Operation successful, False: Otherwise
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_source is not None)
    # </editor-fold>
    try:
      self.abort.emit((True, a_source))
    except Exception as e:
      logger.error(e)
      return False
    else:
      return True
