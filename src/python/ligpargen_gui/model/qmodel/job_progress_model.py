import copy
import logging
import pathlib
from typing import Optional

from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtCore import Qt

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class JobProgressModel(QtGui.QStandardItemModel):
  """Model class for storing the job progress."""

  def __init__(self) -> None:
    """Constructor."""
    super().__init__()
    self.root_node: Optional[QtGui.QStandardItem] = None

  def create_root_node(self) -> None:
    """Creates the root node of the tree model."""
    if self.root_node is not None:
      default_logging.append_to_log_file(logger, "Root node already exists. Nothing to do.", logging.WARNING)
      return
    self.root_node = self.invisibleRootItem()

  def is_empty(self) -> bool:
    """Checks if the model is empty."""
    return True if self.rowCount() == 0 else False

  def add_job_progress_message(self, message: str) -> None:
    """Adds a row to the model from a simple message."""
    if self.root_node is None:
      self.create_root_node()

    tmp_type_item = QtGui.QStandardItem(message)
    tmp_type_item.setFlags(tmp_type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    self.appendRow([tmp_type_item])
