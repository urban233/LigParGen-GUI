"""Module for all custom signals which can be used as arguments either in the main thread or in separate threads."""
import logging
from typing import TYPE_CHECKING
from typing import Callable

from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

if TYPE_CHECKING:
  from ligpargen_gui.internal.data_structures.data_classes import job_summary

logger = default_logging.setup_logger(__file__)
__docformat__ = "google"


class ProgressSignal(QtCore.QObject):
  """Signal for progress reporting."""

  progress = pyqtSignal(tuple)
  """Signal indicating a progress has been made with the form (message, progress value)."""

  def emit_signal(self, a_message: str, a_value: int) -> bool:
    """Emits a signal with a message and a value to update the progress.

    Args:
        a_message (str): The message to update the progress.
        a_value (int): The value to update the progress.

    Returns:
        True: Operation successful, False: Otherwise

    Raises:
        ValueError: If the given value is not between 0 and 100.
    """
    # <editor-fold desc="Checks">
    if a_message is None:
      logger.error("a_message is None.")
      return False
    if a_value is None:
      logger.error("a_value is None.")
      return False
    if a_value < 0 or a_value > 100:
      return False

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

  abort = pyqtSignal(tuple)
  """Signal indicating to abort an operation with the form (bool, source)."""

  def emit_signal(self, a_source: Callable) -> bool:
    """Emits the signal.

    Args:
        a_source (Callable): The function or task where the signal is to be emitted.

    Returns:
        True: Operation successful, False: Otherwise
    """
    # <editor-fold desc="Checks">
    if a_source is None:
      logger.error("a_source is None.")
      return False

    # </editor-fold>

    try:
      self.abort.emit((True, a_source))
    except Exception as e:
      logger.error(e)
      return False
    else:
      return True


class RefreshAfterJobFinishedSignal(QtCore.QObject):
  """Signal for refreshing after a job has finished."""

  refresh = pyqtSignal(tuple)
  """Signal to transfer data after a job finished in the form (job_is_for_current_project_flag, a_job_base_information_object, the_widget)"""

  def emit_signal(
          self,
          job_is_for_current_project_flag: bool,
          a_job_base_information_object: "job_summary.JobBaseInformation",
          the_widget: QtWidgets.QWidget,
  ) -> bool:
    """Emits the signal.

    Args:
        job_is_for_current_project_flag (bool): A flag if the job is for the current project.
        a_job_base_information_object (job_summary.JobBaseInformation): The job's base information.
        the_widget (QtWidgets.QWidget): The widget associated with the signal.

    Returns:
        True: Operation successful, False: Otherwise
    """
    # <editor-fold desc="Checks">
    if job_is_for_current_project_flag is None:
      logger.error("job_is_for_current_project_flag is None.")
      return False
    if a_job_base_information_object is None:
      logger.error("a_job_base_information_object is None.")
      return False
    if the_widget is None:
      logger.error("the_widget is None.")
      return False

    # </editor-fold>

    try:
      self.refresh.emit(
        (
          job_is_for_current_project_flag,
          a_job_base_information_object,
          the_widget,
        )
      )
    except Exception as e:
      logger.error(e)
      return False
    else:
      return True
