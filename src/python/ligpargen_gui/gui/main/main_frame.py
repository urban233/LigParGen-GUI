import logging
import pathlib
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets
from media_forge.gui.custom_widgets import ribbon_bar, side_tabs, custom_button, line_edit_search, custom_panel, \
  split_pane_design
# from ligpargen_gui.model.data_classes import workspace_project
from media_forge.model.preference import model_definitions
from media_forge.model.qmodel import music_model
from media_forge.model.util.gui_style import icons
from media_forge.gui.main.forms.auto import auto_main_frame
from media_forge.gui.custom_widgets import popup_dialog
# from ligpargen_gui.model.util import exception
# from ligpargen_gui.model.pymmm_logging import default_logging

#logger = default_logging.setup_logger(__file__)


class MainFrame(QtWidgets.QMainWindow):
  """Main frame class."""

  dialogClosed = QtCore.pyqtSignal(tuple)
  """A signal indicating that the dialog is closed."""

  def __init__(self, a_tidal_session) -> None:
    """Constructor."""
    super().__init__()
    # build ui object
    self.ui = auto_main_frame.Ui_MainWindow()
    self.ui.setupUi(self)
    # Custom widgets
    self.ribbon_bar = ribbon_bar.RibbonBar()
    self.add_custom_ribbon()
    self.btn_blank_project = custom_button.BigCardButton("Blank Space")
    self.add_blank_project_button()
    shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(8)
    shadow_effect.setOffset(3, 3)
    shadow_effect.setColor(QtGui.QColor(0, 0, 0, 15))
    self.ui.main_content_frame.setGraphicsEffect(shadow_effect)
    self.ui.main_content_frame.setStyleSheet(
      """QFrame#main_content_frame {
        border: 1px solid white;
        background: white;
        margin: 5px;
        border-radius: 10px;
      }
      """
    )

    self.music_model = music_model.MusicModel.from_a_directory(pathlib.Path(r"C:\Users\hannah\github_repos\MediaForge\test_files\music"))

    self.list_widget = QtWidgets.QWidget()
    tmp_list_layout = QtWidgets.QVBoxLayout()
    self.list_view = QtWidgets.QListView()
    self.list_view.setModel(self.music_model.get_album_artist_model())
    self.list_label = QtWidgets.QLabel("Album Artist")
    tmp_list_layout.addWidget(self.list_label)
    tmp_list_layout.addWidget(self.list_view)
    self.list_widget.setLayout(tmp_list_layout)
    self.list_widget.setMaximumWidth(275)

    self.table_widget = QtWidgets.QWidget()
    tmp_table_layout = QtWidgets.QVBoxLayout()
    self.table_view = QtWidgets.QTableView()
    self.table_view.setModel(self.music_model)
    self.table_view.resizeColumnsToContents()
    header = self.table_view.horizontalHeader()
    header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    # Set the resize mode for each column
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
    self.table_label = QtWidgets.QLabel("Tracks")
    tmp_table_layout.addWidget(self.table_label)
    tmp_table_layout.addWidget(self.table_view)
    self.table_widget.setLayout(tmp_table_layout)

    self.side_panel_search_tidal = custom_panel.SearchTidal(a_tidal_session)
    self.side_panel_running_jobs = custom_panel.RunningJobsPanel()
    self.side_panel_completed_jobs = custom_panel.CompletedJobsPanel()

    self.side_panel_stacked_widget = QtWidgets.QStackedWidget()
    self.side_panel_stacked_widget.addWidget(self.side_panel_search_tidal)
    self.side_panel_stacked_widget.addWidget(self.side_panel_running_jobs)
    self.side_panel_stacked_widget.addWidget(self.side_panel_completed_jobs)

    self.bottom_panel = custom_panel.CustomBottomPanel("Bottom Panel Test")

    self.split_pane = split_pane_design.SplitPaneDesign(
      [self.list_widget, self.table_widget],
      self.side_panel_stacked_widget,
      self.bottom_panel
    )
    self.ui.horizontalLayout.addWidget(self.split_pane)
    self.split_pane.hide_bottom_panel()
    # Init gui
    self.init_ui()
    self.line_edit_search = line_edit_search.LineEditSearch(self)
    self.ui.verticalLayout_55.insertWidget(0, self.line_edit_search)
    self.ui.stackedWidget.setCurrentIndex(1)

  def set_tab_texts_for_project_page(self,
                                     tab_texts: list[tuple[str, Optional["model_definitions.IconsEnum"]]]) -> None:
    """Sets the tab text for all tabs on the project page."""
    for i, tmp_tab_text in enumerate(tab_texts):
      self.ui.tab_widget_project_page.tabBar().setTabText(i, "")
      self.ui.tab_widget_project_page.tabBar().setTabButton(
        i, QtWidgets.QTabBar.ButtonPosition.LeftSide,
        side_tabs.SideTabs(tmp_tab_text[0], tmp_tab_text[1])
      )

  def set_custom_stylesheet_for_project_page_tab_widget(self):
    """Sets custom stylesheet for the project page tab widget."""
    self.ui.tab_widget_project_page.setStyleSheet(
      """
      QTabWidget::pane { /* The tab widget frame */
          border: 1px solid #DCDBE3;
          background: #f5f5f5;
          margin: 0px;
          padding: 0px;
      }
  
      QTabWidget::tab-bar {
          left: 0px; /* move to the right by 5px */
      }
  
      QTabBar::tab {
          border: none;
          border-radius: 0px;
          background: #f0f0f0;
          min-width: 70px;
          max-width: 70px;
          font-size: 13px;
          padding: 0px;
          padding-top: 5px;
          padding-bottom: 5px;
          padding-right: 30px;
      }
  
      QTabBar::tab:selected, QTabBar::tab:hover {
          background: #e6e6e6;
          border: 2px solid #B8B8B8;
          border-top: none;
          border-bottom: none;
          border-right: none;
      }
  
      QTabBar::tab:selected {
          border-color: #367AF6;
          background: #e6e6e6;
          font: bold;
      }
  
      QTabBar::tab:!selected {
          margin-top: 0px
      }
  
      QToolButton {
          background-color: white;
          /*min-width: 1.5em;*/
          min-width: 24px;
          min-height: 24px;
          max-height: 64px;
          padding: 0px;
          border: none;
      }
  
      QToolButton::hover {
          background: #f5f5f5;
          color: black;
      }
      """
    )

  def eventFilter(self, obj, event):
    if event.type() == QtCore.QEvent.Type.MouseButtonPress:
      # Close the dialog if the click is outside the dialog and QLineEdit
      if self.line_edit_search.search_dialog.isVisible():
        self.line_edit_search.search_dialog.hide()
    return super().eventFilter(obj, event)

  # <editor-fold desc="Basic">
  def closeEvent(self, event) -> None:  # noqa: ANN001
    """Overrides the closeEvent of the QMainWindow class.

    Args:
        event: The event object representing the close event.
    """
    # <editor-fold desc="Checks">
    # if event is None:
    #   logger.error("event is None.")
    #   raise exception.IllegalArgumentError("event is None.")

    # </editor-fold>
    # Emit the custom signal when the window is closed
    self.dialogClosed.emit(("", event))

  def init_ui(self) -> None:
    """Initialize the UI elements."""
    self.set_tab_texts_for_project_page(
      [
        ("Home", model_definitions.IconsEnum.HOME),
        ("New", model_definitions.IconsEnum.NEW),
        ("Open", model_definitions.IconsEnum.OPEN),
        ("Delete", model_definitions.IconsEnum.DELETE),
        ("Close", model_definitions.IconsEnum.CLOSE),
        ("Import", model_definitions.IconsEnum.IMPORT),
        ("Export", model_definitions.IconsEnum.EXPORT),
        ("Settings", None),
        ("Exit", None)
      ]
    )
    self.set_custom_stylesheet_for_project_page_tab_widget()
    self.set_icons()

  def set_icons(self) -> None:
    """Sets all icons for the main frame."""
    # <editor-fold desc="Help">
    icons.set_icon(self.ui.btn_help_5, model_definitions.IconsEnum.HELP)
    icons.set_icon(self.ui.btn_help_6, model_definitions.IconsEnum.HELP)
    icons.set_icon(self.ui.btn_help_7, model_definitions.IconsEnum.HELP)
    icons.set_icon(self.ui.btn_help_8, model_definitions.IconsEnum.HELP)
    # </editor-fold>
    icons.set_icon(self.ui.btn_scroll_area_delete_delete, model_definitions.IconsEnum.DELETE)
    icons.set_icon(self.ui.btn_project_page_back, model_definitions.IconsEnum.BACK)
    self.ui.btn_project_page_back.setStyleSheet(
      """
      QPushButton#btn_project_page_back {
          background-color: white;
          border: 1px solid #5f6368;
          border-radius: 13px;
          border-color: #5f6368;
          padding: 2px;
          margin-top: 10px;
          margin-left: 10px;
          margin-right: 20px;
          min-width: 20px;
          max-width: 20px;
          min-height: 20px;
          max-height: 20px
      }
      """
    )
  # </editor-fold>

  # <editor-fold desc="Add custom widgets">
  def add_custom_ribbon(self):
    """Adds a custom Microsoft style ribbon widget to the main frame."""
    self.ui.verticalLayout.insertWidget(0, self.ribbon_bar)

  def add_blank_project_button(self):
    self.ui.scroll_area_new_project_layout.insertWidget(0, self.btn_blank_project)

  def add_custom_pop_up_dialogs(self):
    """Adds custom pop-up dialogs to the main frame."""
    # Add custom scene dropdown
    self.drop_down = popup_dialog.ScenesPopUpDialog(self)
    self.import_popup = popup_dialog.ImportPopUpDialog(self)

  def fill_open_project_scroll_area(self, the_project_model: QtGui.QStandardItemModel, a_callable):
    for i in range(the_project_model.rowCount()):
      tmp_workspace_project: "workspace_project.WorkspaceStorageSpace" = the_project_model.data(the_project_model.index(i, 0), model_definitions.RolesEnum.OBJECT_ROLE)
      self.ui.scroll_area_open_project_layout.insertWidget(
        i + 1,
        tmp_workspace_project.get_as_button(a_callable)
      )
    self.ui.lbl_scroll_area_open_project_name.setStyleSheet("margin-left: 10px;")
    self.ui.lbl_scroll_area_open_project_date_modified.setStyleSheet("margin-right: 25px;")

  def fill_home_project_scroll_area(self, the_project_model: QtGui.QStandardItemModel, a_callable):
    for i in range(the_project_model.rowCount()):
      if i < 11:
        tmp_workspace_project: "workspace_project.WorkspaceStorageSpace" = the_project_model.data(the_project_model.index(i, 0), model_definitions.RolesEnum.OBJECT_ROLE)
        self.ui.scroll_area_home_project_layout.insertWidget(
          i + 1,
          tmp_workspace_project.get_as_button(a_callable)
        )
    self.ui.lbl_scroll_area_home_project_name.setStyleSheet("margin-left: 10px;")
    self.ui.lbl_scroll_area_home_project_date_modified.setStyleSheet("margin-right: 25px;")
  # </editor-fold>

  # <editor-fold desc="Pop-up related">
  def show_menu(self) -> None:
    """Shows the dropdown menu for the scene selection."""
    # Determine the position to show the dialog (beneath the button)
    button_pos = self.ui.btn_scene_name.mapToGlobal(QtCore.QPoint(0, self.ui.btn_scene_name.height()))
    self.drop_down.move(button_pos)
    self.drop_down.show()

  def show_import_popup(self) -> None:
    """Shows the dropdown menu for the scene selection."""
    # Show the dialog momentarily to ensure its size is calculated
    self.import_popup.adjustSize()
    # Get the button's position in global coordinates
    button_pos = self.ui.btn_import_seq.mapToGlobal(QtCore.QPoint(0, 0))
    # Subtract the dialog's height to position it above the button
    dialog_height = self.import_popup.height()
    adjusted_pos = button_pos - QtCore.QPoint(0, dialog_height)
    # Move the dialog to the adjusted position
    self.import_popup.move(adjusted_pos)
    self.import_popup.show()
  # </editor-fold>
