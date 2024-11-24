import logging
from typing import Optional, Any

from PyQt6 import QtGui
from PyQt6 import QtCore

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import exception, safeguard
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class BaseTreeModel(QtGui.QStandardItemModel):
  """Base class for tree model classes"""

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
    """Checks if the model is empty.

    Returns:
      True if the row count is 0, Otherwise: False.
    """
    return True if self.rowCount() == 0 else False

  def add_node(
    self,
    a_parent_node: QtGui.QStandardItem,
    an_item_name: str,
    an_item_type_value: "model_definitions.TypesEnum",
    an_item_object_value: Optional[object] = None
  ) -> QtGui.QStandardItem:
    """Adds a node to the tree model.

    Args:
      a_parent_node: A node where the new node will be added.
      an_item_name: A name for the new node.
      an_item_type_value: A value for the "type" role of the new node.
      an_item_object_value: A value for the "object" role of the new node.

    Returns:
      A QStandardItem that contains all given information.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_parent_node is not None)
    safeguard.CHECK(an_item_name is not None)
    safeguard.CHECK(an_item_name != "")
    safeguard.CHECK(an_item_type_value is not None)
    safeguard.CHECK(an_item_object_value is not None)
    # </editor-fold>
    tmp_item = QtGui.QStandardItem(an_item_name)
    if an_item_object_value is not None:
      tmp_item.setData(an_item_object_value, model_definitions.RolesEnum.OBJECT_ROLE)
    tmp_item.setData(an_item_type_value, model_definitions.RolesEnum.TYPE_ROLE)
    a_parent_node.appendRow(tmp_item)
    return tmp_item

  def remove_node(self, a_model_index: QtCore.QModelIndex) -> None:
    """Removes a node for a given model index.

    Args:
      a_model_index: The index of the item to be removed.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_model_index is not None)
    # </editor-fold>
    tmp_item = self.itemFromIndex(a_model_index)
    self.removeRow(tmp_item.row())

  def get_index(self, a_row: int, a_parent: Optional[QtCore.QModelIndex] = None) -> QtCore.QModelIndex:
    """Gets an index based on the given row and optionally parent index.

    Args:
      a_row: The row to get the index for
      a_parent: The parent index to set the row in context (Default: None)

    Returns:
      A QModelIndex that contains the given row and optionally parent index.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_row is not None)
    safeguard.CHECK(a_row > 0)
    # </editor-fold>
    if a_parent is None:
      return self.index(a_row, 0)
    return self.index(a_row, 0, a_parent)

  def get_root_node_as_index(self) -> QtCore.QModelIndex:
    """Returns the root node as a QModelIndex.

    Returns:
      A QModelIndex that contains the root node.
    """
    return self.indexFromItem(self.root_node)

  def get_display_data_of_index(self, an_index: QtCore.QModelIndex) -> str:
    """Gets the display data of the index.

    Args:
      an_index: The index to get the type of

    Returns:
      The display role as string of the given index.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(an_index is not None)
    # </editor-fold>
    return an_index.data(QtCore.Qt.ItemDataRole.DisplayRole)

  def get_type_data_of_index(self, an_index: QtCore.QModelIndex) -> str:
    """Gets the type of the index.

    Args:
      an_index: The index to get the type of

    Returns:
      The type role as string of the given index.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(an_index is not None)
    # </editor-fold>
    return an_index.data(model_definitions.RolesEnum.TYPE_ROLE)

  def get_object_data_of_index(self, an_index: QtCore.QModelIndex) -> Any:
    """Gets the object of the index.

    Args:
      an_index: The index to get the object of

    Returns:
      The saved data object of the given index.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(an_index is not None)
    # </editor-fold>
    return an_index.data(model_definitions.RolesEnum.OBJECT_ROLE)

  def create_row_number_iterator(self, an_index: Optional[QtCore.QModelIndex] = None) -> range:
    """Creates a list of row numbers for the given index.

    Args:
      an_index: The index of which the children rows should be used (Default: None)

    Returns:
      A range iterator of the row count.
    """
    if an_index is None:
      return range(self.rowCount())
    return range(self.rowCount(an_index))
