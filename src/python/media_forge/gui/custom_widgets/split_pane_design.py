from PyQt6 import QtWidgets, QtCore


class SplitPaneDesign(QtWidgets.QWidget):
  """Class representing a split pane design widget."""

  def __init__(self, main_panel_widgets: list, a_side_panel_stacked_widget, a_bottom_panel) -> None:
    """Constructor."""
    super().__init__()
    self.main_panel_widgets = main_panel_widgets
    self.side_panel_stacked_widget = a_side_panel_stacked_widget
    self.bottom_panel = a_bottom_panel

    self.splitter_main_panel = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
    self.splitter_bottom_panel = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
    self.splitter_side_panel = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

    for tmp_main_panel_widget in self.main_panel_widgets:
      self.splitter_main_panel.addWidget(tmp_main_panel_widget)
    self.splitter_bottom_panel.addWidget(self.splitter_main_panel)
    self.splitter_bottom_panel.addWidget(a_bottom_panel)

    self.main_panel_container = QtWidgets.QWidget()
    self.main_panel_container_layout = QtWidgets.QVBoxLayout()
    self.main_panel_container_layout.addWidget(self.splitter_bottom_panel)
    self.main_panel_container.setLayout(self.main_panel_container_layout)

    self.splitter_side_panel.addWidget(self.main_panel_container)
    self.splitter_side_panel.addWidget(a_side_panel_stacked_widget)

    self.main_layout = QtWidgets.QHBoxLayout()
    self.main_layout.addWidget(self.splitter_side_panel)
    self.setLayout(self.main_layout)
    self.setContentsMargins(0, 0, 0, 0)

  def hide_bottom_panel(self) -> None:
    """Hides the bottom panel."""
    self.bottom_panel.hide()
