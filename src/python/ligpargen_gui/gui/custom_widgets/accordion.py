import logging

from PyQt6 import QtCore
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFrame

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import exception
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

    Raises:
      exception.NoneValueError: If any of the arguments are None.
      exception.IllegalArgumentError: If `a_title` is an empty string.
    """
    # <editor-fold desc="Checks">
    if a_title is None:
      default_logging.append_to_log_file(logger, "a_title is None.", logging.ERROR)
      raise exception.NoneValueError("a_title is None.")
    if a_title == "":
      default_logging.append_to_log_file(logger, "a_title is an empty string.", logging.ERROR)
      raise exception.IllegalArgumentError("a_title is an empty string.")
    if a_content_widget is None:
      default_logging.append_to_log_file(logger, "a_content_widget is None.", logging.ERROR)
      raise exception.NoneValueError("a_content_widget is None.")
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

  def __init__(self, accordion_sections: list["AccordionSection"]):
    """Constructor.

    Args:
      accordion_sections: A list of AccordionSection objects.

    Raises:
      exception.NoneValueError: If `accordion_sections` is None.
    """
    # <editor-fold desc="Checks">
    if accordion_sections is None:
      default_logging.append_to_log_file(logger, "accordion_sections is None.", logging.ERROR)
      raise exception.NoneValueError("accordion_sections is None.")
    # </editor-fold>
    super().__init__()
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    for tmp_accordion_section in accordion_sections:
      layout.addWidget(tmp_accordion_section)
    self.setLayout(layout)

  # def __init__(self):
  #   super().__init__()
  #
  #   layout = QVBoxLayout()
  #
  #   # Create content for first section
  #   content1 = QWidget()
  #   content1_layout = QVBoxLayout()
  #   content1_layout.addWidget(QPushButton("Option 1"))
  #   content1_layout.addWidget(QPushButton("Option 2"))
  #   content1.setLayout(content1_layout)
  #
  #   # First section
  #   section1 = AccordionSection("Image Size", content1)
  #
  #   # Create content for second section
  #   content2 = QWidget()
  #   content2_layout = QVBoxLayout()
  #   content2_layout.addWidget(QPushButton("Option A"))
  #   content2_layout.addWidget(QPushButton("Option B"))
  #   content2.setLayout(content2_layout)
  #
  #   # Second section
  #   section2 = AccordionSection("Position", content2)
  # 1
  #   # Add sections to the main layout
  #   layout.addWidget(section1)
  #   layout.addWidget(section2)
  #
  #   layout.addStretch()  # To push content to the top
  #   layout.setContentsMargins(0, 0, 0, 0)
  #   self.setLayout(layout)
