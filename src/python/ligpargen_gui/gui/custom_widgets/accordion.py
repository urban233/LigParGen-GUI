import logging

from PyQt6 import QtCore
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFrame

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import exception, safeguard
from ligpargen_gui.model.util.gui_style import icons
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class AccordionSection(QWidget):
  """Represents a single section within the accordion widget."""

  def __init__(self, a_title: str, a_content_widget: QWidget) -> None:
    """Constructor.

    Args:
      a_title: The title of the section.
      a_content_widget: The content widget of the section.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_title is not None)
    safeguard.CHECK(a_title != "")
    safeguard.CHECK(a_content_widget is not None)
    # </editor-fold>
    super().__init__()

    self.button = QPushButton(a_title)
    self.button.setIcon(icons.get_icon(model_definitions.IconsEnum.TREE_EXPAND))
    self.button.setIconSize(self.button.icon().actualSize(QtCore.QSize(32, 32)))
    self.button.setStyleSheet(
      """
      QPushButton {
          background-color: rgba(220, 219, 227, 0.01);
          border: none;
          border-radius: 4px;
          text-align: left;
      }
      QPushButton::hover {
          background-color: rgba(220, 219, 227, 0.5);
          border: none;
      }
      """
    )

    self.content = a_content_widget
    self.content.setVisible(False)  # Start with content hidden

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.button)
    layout.addWidget(self.content)

    self.setLayout(layout)

    self.button.clicked.connect(self.toggle_content)

  def toggle_content(self) -> None:
    """Toggles the visibility of the section's content."""
    if self.content.isVisible():
      self.button.setIcon(icons.get_icon(model_definitions.IconsEnum.TREE_EXPAND))
    else:
      self.button.setIcon(icons.get_icon(model_definitions.IconsEnum.TREE_COLLAPSE))
    self.content.setVisible(not self.content.isVisible())


class AccordionWidget(QWidget):
  """Represents the container for multiple AccordionSection objects."""

  def __init__(self, accordion_sections: list["AccordionSection"]) -> None:
    """Constructor.

    Args:
      accordion_sections: A list of AccordionSection objects.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(accordion_sections is not None)
    # </editor-fold>
    super().__init__()
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    for tmp_accordion_section in accordion_sections:
      layout.addWidget(tmp_accordion_section)
    self.setLayout(layout)
