from PyQt6 import QtCore
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFrame

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import icons


class AccordionSection(QWidget):
  def __init__(self, title, content_widget):
    super().__init__()

    self.button = QPushButton(title)
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

    self.content = content_widget
    self.content.setVisible(False)  # Start with content hidden

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.button)
    layout.addWidget(self.content)

    self.setLayout(layout)

    self.button.clicked.connect(self.toggle_content)

  def toggle_content(self):
    if self.content.isVisible():
      self.button.setIcon(icons.get_icon(model_definitions.IconsEnum.TREE_EXPAND))
    else:
      self.button.setIcon(icons.get_icon(model_definitions.IconsEnum.TREE_COLLAPSE))
    self.content.setVisible(not self.content.isVisible())


class AccordionWidget(QWidget):

  def __init__(self, accordion_sections: list["AccordionSection"]):
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
