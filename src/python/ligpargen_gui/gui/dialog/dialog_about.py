"""Module for the About dialog."""
from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6 import QtCore
from ligpargen_gui.gui.dialog.forms.auto.auto_dialog_about import Ui_Dialog
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import styles_utils


class DialogAbout(QtWidgets.QDialog):
  """Class representing an About dialog."""

  def __init__(self, parent=None) -> None:  # noqa: ANN001
    """Constructor.

    Args:
        parent: The parent.
    """
    QtWidgets.QDialog.__init__(self, parent)
    # build ui object
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)

    self.ui.btn_ok.clicked.connect(self.close_dialog)
    original_pixmap = QtGui.QPixmap(str(model_definitions.ModelDefinitions.LOGO_FILEPATH))
    scaled_pixmap = original_pixmap.scaled(150, 150)
    self.ui.lbl_pyssa_logo.setPixmap(scaled_pixmap)
    styles_utils.set_stylesheet(self)
    self.ui.label_2.setText(f"Version: {model_definitions.ModelDefinitions.VERSION_NUMBER}")
    self.ui.label_2.setStyleSheet("font-weight: bold;")
    self.ui.label.setStyleSheet("font-size: 19px")

    self._fill_table_view()

    self.setWindowIcon(QtGui.QIcon(str(model_definitions.ModelDefinitions.LOGO_FILEPATH)))
    self.setWindowTitle("About")
    self.setWindowFlags(
      self.windowFlags() & ~QtCore.Qt.WindowType.WindowContextHelpButtonHint
    )

  def _fill_table_view(self) -> None:
    """Fill the table with the packages."""
    tmp_table_model = QtGui.QStandardItemModel()
    tmp_table_model.setHorizontalHeaderLabels(["Name", "Version", "License"])
    # Sample data
    data = [
        ["Material Design 3 Icons", "4.0.0", "Apache License 2.0"],
        ["Numpy", "2.1.2", "BSD 3-Clause 'New' or 'Revised' License"],
        ["ZeroMQ", "26.2.0", "BSD 3-Clause License"],
        ["PyQt6", "6.7.1", "GNU General Public License (GPL)"],
    ]

    # Populate the model with data
    for row, row_data in enumerate(data):
      for col, value in enumerate(row_data):
        item = QtGui.QStandardItem(
            str(value)
        )  # or QStandardItem(str(value)) for QStandardItemModel
        tmp_table_model.setItem(row, col, item)
    self.ui.tableView.setModel(tmp_table_model)
    self.ui.tableView.resizeColumnsToContents()
    self.ui.tableView.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)

  def close_dialog(self) -> None:
    """Closes the dialog."""
    self.close()
