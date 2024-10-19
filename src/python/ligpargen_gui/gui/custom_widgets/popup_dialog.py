from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets

from ligpargen_gui.gui.custom_widgets import custom_button
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import icons


class BasePopUpDialog(QtWidgets.QDialog):

  def __init__(self, a_window_title: str, parent=None):
    super().__init__(parent, QtCore.Qt.WindowType.Popup)  # Use Popup to behave like a drop-down
    self.setWindowTitle(a_window_title)


class ChooseResultFilesPopUpDialog(BasePopUpDialog):
  def __init__(self, a_title, actions: list[QtGui.QAction], parent=None):
    super().__init__("", parent)
    self.setStyleSheet("""
        QDialog {
            background-color: white; 
            border: 2px solid #e0e0e0; 
            border-radius: 4px;
        }
        QMenu {
            background-color: white;
            margin: 2px; /* some spacing around the menu */ 
        }
        QMenu::item {
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 7px;
            padding-right: 15px;
            font-size: 13px;
        }
        QMenu::item:selected {
            background: #D6E4FD;
            border-width: 2px;
            border-radius: 4px;
            border-color: white;
        }
        QMenu::icon {
            padding-left: 15px;  /* Add left padding to the icon */
        }
        QMenu::separator {
            height: 1px;
            background: #E2E2E2;
            margin-left: 0px;
            margin-right: 0px;
        }
        QLabel {
            padding-top: 5px;
            padding-bottom: 5px;
            padding-right: 10px;
            margin-left: 10px;
            font: bold;
            font-size: 12px;
            color: #242424;
        }
    """)
    # Set up the menu
    layout = QtWidgets.QVBoxLayout(self)
    self.menu = QtWidgets.QMenu()
    # Create a non-clickable descriptive text using QWidgetAction
    self.descriptive_text = QtWidgets.QLabel(a_title)
    #self.descriptive_text.setStyleSheet("padding: 0px 10px; color: black; font: bold;")
    widget_action = QtWidgets.QWidgetAction(self)
    widget_action.setDefaultWidget(self.descriptive_text)
    #self.menu.addAction(widget_action)
    # Create actions
    # Add actions to the menu
    for tmp_action in actions:
      self.menu.addAction(tmp_action)
    layout.addWidget(self.menu)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

# class ChooseGromacsResultFilesPopUpDialog(BasePopUpDialog):
#   def __init__(self, a_title, parent=None):
#     super().__init__("", parent)
#     self.setStyleSheet("""
#         QDialog {
#             background-color: white;
#             border: 2px solid #e0e0e0;
#             border-radius: 4px;
#         }
#         QMenu {
#             background-color: white;
#             margin: 2px; /* some spacing around the menu */
#         }
#         QMenu::item {
#             padding-top: 5px;
#             padding-bottom: 5px;
#             padding-left: 7px;
#             padding-right: 15px;
#             font-size: 13px;
#         }
#         QMenu::item:selected {
#             background: #D6E4FD;
#             border-width: 2px;
#             border-radius: 4px;
#             border-color: white;
#         }
#         QMenu::icon {
#             padding-left: 15px;  /* Add left padding to the icon */
#         }
#         QMenu::separator {
#             height: 1px;
#             background: #E2E2E2;
#             margin-left: 0px;
#             margin-right: 0px;
#         }
#         QLabel {
#             padding-top: 5px;
#             padding-bottom: 5px;
#             padding-right: 10px;
#             margin-left: 10px;
#             font: bold;
#             font-size: 12px;
#             color: #242424;
#         }
#     """)
#     # Set up the menu
#     layout = QtWidgets.QVBoxLayout(self)
#     self.menu = QtWidgets.QMenu()
#     # Create a non-clickable descriptive text using QWidgetAction
#     self.descriptive_text = QtWidgets.QLabel(a_title)
#     #self.descriptive_text.setStyleSheet("padding: 0px 10px; color: black; font: bold;")
#     widget_action = QtWidgets.QWidgetAction(self)
#     widget_action.setDefaultWidget(self.descriptive_text)
#     #self.menu.addAction(widget_action)
#     # Create actions
#     # Add actions to the menu
#     self.action_gromacs_param = QtGui.QAction(".gro", self)
#     self.action_gromacs_param.setCheckable(True)
#     self.action_gromacs_top = QtGui.QAction(".itp", self)
#     self.action_gromacs_top.setCheckable(True)
#     self.menu.addAction(self.action_gromacs_param)
#     self.menu.addAction(self.action_gromacs_top)
#     layout.addWidget(self.menu)
#     layout.setContentsMargins(0, 0, 0, 0)
#     layout.setSpacing(0)


class ScenesPopUpDialog(BasePopUpDialog):

  def __init__(self, parent=None):
    super().__init__("All Scenes", parent)
    self.setFixedSize(300, 400)
    layout = QtWidgets.QVBoxLayout(self)
    self.list_view = QtWidgets.QListView(self)
    layout.addWidget(self.list_view)
    # Example items for the list view
    self.model = QtCore.QStringListModel(["Option 1", "Option 2", "Option 3"])
    self.list_view.setModel(self.model)


class ImportPopUpDialog(BasePopUpDialog):
  def __init__(self, parent=None):
    super().__init__("Import From", parent)
    self.setStyleSheet("""
        QDialog {
            background-color: white; 
            border: 2px solid #e0e0e0; 
            border-radius: 4px;
        }
        QMenu {
            background-color: white;
            margin: 2px; /* some spacing around the menu */ 
        }
        QMenu::item {
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 7px;
            padding-right: 15px;
            font-size: 13px;
        }
        QMenu::item:selected {
            background: #D6E4FD;
            border-width: 2px;
            border-radius: 4px;
            border-color: white;
        }
        QMenu::icon {
            padding-left: 15px;  /* Add left padding to the icon */
        }
        QMenu::separator {
            height: 1px;
            background: #E2E2E2;
            margin-left: 0px;
            margin-right: 0px;
        }
        QLabel {
            padding-top: 5px;
            padding-bottom: 5px;
            padding-right: 10px;
            margin-left: 10px;
            font: bold;
            font-size: 12px;
            color: #242424;
        }
    """)
    # Set up the menu
    layout = QtWidgets.QVBoxLayout(self)
    self.menu = QtWidgets.QMenu()
    # Create a non-clickable descriptive text using QWidgetAction
    self.descriptive_text = QtWidgets.QLabel("Import Sequence From")
    #self.descriptive_text.setStyleSheet("padding: 0px 10px; color: black; font: bold;")
    widget_action = QtWidgets.QWidgetAction(self)
    widget_action.setDefaultWidget(self.descriptive_text)
    self.menu.addAction(widget_action)
    # Create actions
    self.action_copy_paste = QtGui.QAction("Copy + Paste", self)
    self.action_copy_paste.setIcon(icons.get_icon(model_definitions.IconsEnum.IMPORT_SEQUENCE))
    self.action_this_device = QtGui.QAction("This Device", self)
    self.action_this_device.setIcon(icons.get_icon(model_definitions.IconsEnum.IMPORT_SEQUENCE))
    # Add actions to the menu
    self.menu.addAction(self.action_copy_paste)
    self.menu.addAction(self.action_this_device)
    layout.addWidget(self.menu)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)


class StatusPopup(QtWidgets.QWidget):
  def __init__(self, message, parent=None):
    super().__init__(parent)
    self.setWindowFlags(QtCore.Qt.WindowType.ToolTip)  # Make it behave like a tooltip
    #self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # Optional for style

    # Layout and label for the message
    layout = QtWidgets.QVBoxLayout()
    self.lbl_message = QtWidgets.QLabel(message)
    layout.addWidget(self.lbl_message)
    self.setLayout(layout)
    self.adjustSize()
