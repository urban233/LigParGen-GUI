
import requests
from PyQt6 import QtWidgets, QtGui, QtCore
from tidalapi import media

from media_forge.gui.custom_widgets import accordion, custom_accordion_sections
from media_forge.model.preference import model_definitions
from media_forge.model.qmodel import search_model
from media_forge.model.util.gui_style import icons


class CustomSidePanel(QtWidgets.QWidget):
  """Class to create custom side panels for the main frame."""

  panelClosed = QtCore.pyqtSignal()
  """A signal indicating that the panel is closed."""
  panelOpened = QtCore.pyqtSignal()
  """A signal indicating that the panel is opened."""

  def __init__(self, a_title: str) -> None:
    """Constructor."""
    super().__init__()
    self.btn_close = QtWidgets.QPushButton()
    icons.set_icon(self.btn_close, model_definitions.IconsEnum.CLOSE)
    self.btn_close.setStyleSheet(
      """
      QPushButton {
          background-color: rgba(220, 219, 227, 0.01);
          border: none;
          border-radius: 4px;
          min-width: 36px;
          max-width: 36px;
          min-height: 36px;
          max-height: 36px;
      }
      QPushButton::hover {
          background-color: rgba(220, 219, 227, 0.5);
          border: none;
          min-width: 40px;
          max-width: 40px;
          min-height: 40px;
          max-height: 40px;
      }
      """
    )
    self.lbl_header = QtWidgets.QLabel(a_title)
    self.lbl_header.setStyleSheet(
      """
      QLabel {
        font-size: 20px;
        margin-left: 8px;
      }
      """
    )
    self.layout_header = QtWidgets.QHBoxLayout()
    self.layout_header.addWidget(self.lbl_header)
    self.layout_header.addStretch()
    self.layout_header.addWidget(self.btn_close)

    self.content_frame = QtWidgets.QFrame()
    self.layout_content_frame = QtWidgets.QVBoxLayout()
    self.content_frame.setLayout(self.layout_content_frame)

    self.global_layout = QtWidgets.QVBoxLayout()
    self.global_layout.addLayout(self.layout_header)
    self.global_layout.addWidget(self.content_frame)
    self.setLayout(self.global_layout)
    self.btn_close.clicked.connect(self.hide_panel)

  def add_global_stretch(self):
    """Adds a stretch to the bottom of the global layout."""
    self.global_layout.addStretch()

  def hide_panel(self):
    """Hides the entire panel."""
    self.panelClosed.emit()

  def show_panel(self):
    """Shows the entire panel."""
    self.panelOpened.emit()


class SearchTidal(CustomSidePanel):
  """Custom panel for searching tidal."""

  def __init__(self, a_tidal_session) -> None:
    """Constructor"""
    super().__init__("Download from Tidal")
    self.tidal_session = a_tidal_session
    self.search_model = search_model.SearchModel()

    self.tab_widget = QtWidgets.QTabWidget()
    self.albums_tab = QtWidgets.QWidget()

    self.tracks_tab = QtWidgets.QWidget()
    self.tracks_tab_layout = QtWidgets.QVBoxLayout()
    self.tracks_tab.setLayout(self.tracks_tab_layout)

    self.artists_tab = QtWidgets.QWidget()

    # <editor-fold desc="Search accordion section">
    self.search_tidal_tracks = custom_accordion_sections.SearchTableTidal(self.search_model, self.tidal_session)
    self.search_tidal_tracks.connect_search_tracks_table_view_clicked(self.set_track_information)
    self.accordion_section_search = accordion.AccordionSection(
      "Search Tracks", self.search_tidal_tracks
    )
    # </editor-fold>

    # <editor-fold desc="Track Information accordion section">
    self.tidal_track_information = custom_accordion_sections.TrackInformationTidal()
    self.accordion_section_track_info = accordion.AccordionSection(
      "Track Information", self.tidal_track_information
    )
    # </editor-fold>

    # <editor-fold desc="Add to Job Information accordion section">
    self.tidal_tracks_to_job = custom_accordion_sections.JobTableTidal(self.search_model, self.tidal_session)
    self.tidal_tracks_to_job.connect_tracks_to_job_table_view_clicked(self.set_track_information)
    self.accordion_section_add_to_job_information = accordion.AccordionSection(
      "Add to job", self.tidal_tracks_to_job
    )
    # </editor-fold>

    self.accordion = accordion.AccordionWidget(
      [self.accordion_section_search, self.accordion_section_track_info, self.accordion_section_add_to_job_information]
    )

    self.tracks_tab_layout.addWidget(self.accordion)
    self.tracks_tab_layout.addStretch()
    self.tracks_tab_scroll_area = QtWidgets.QScrollArea()
    self.tracks_tab_scroll_area.setWidgetResizable(True)
    self.tracks_tab_scroll_area.setWidget(self.tracks_tab)

    self.tab_widget.setIconSize(QtCore.QSize(24, 24))
    self.tab_widget.addTab(self.albums_tab, None)
    self.tab_widget.addTab(self.tracks_tab_scroll_area, None)
    self.tab_widget.addTab(self.artists_tab, None)
    self.tab_widget.setTabIcon(0, icons.get_icon(model_definitions.IconsEnum.ALBUM))
    self.tab_widget.setTabIcon(1, icons.get_icon(model_definitions.IconsEnum.MUSIC_NOTE))
    self.tab_widget.setTabIcon(2, icons.get_icon(model_definitions.IconsEnum.ARTIST))
    self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #f0f0f0;
                border-bottom-color: #f0f0f0; /* same as the pane color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border-radius: 4px;
                width: 24px;
                height: 24px;
                margin: 5px;
                padding: 5px; 
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #fafafa;
            }
            QTabBar::tab:selected {
                background: white;
                border-color: #616161;
                border-bottom-color: #367AF6; /* same as pane color */
                border-bottom: 2px solid #367AF6;
            }
            QTabWidget::tab-bar {
                left: 0px;
            }
            QTabWidget::pane { /* The tab widget frame */
                border: 2px solid #DCDBE3;
                border-radius: 4px;
                background: #f0f0f0;
            }
        """)

    self.layout_content_frame.addWidget(self.tab_widget)

  def set_track_information(self):
    """Sets track information for the selected track."""
    tmp_track: media.Track = self.search_tidal_tracks.search_tracks_table_view.currentIndex().data(model_definitions.RolesEnum.OBJECT_ROLE)
    self.tidal_track_information.track_title.setText(tmp_track.name)
    self.tidal_track_information.track_album_artist.setText(tmp_track.album.artist.name)
    self.tidal_track_information.track_album_name.setText(tmp_track.album.name)
    self.tidal_track_information.album_release_date.setText(str(tmp_track.album.release_date.strftime("%Y-%m-%d")))
    tmp_stream = tmp_track.get_stream()
    tmp_manifest = tmp_stream.get_stream_manifest()
    self.tidal_track_information.track_audio_quality.setText(f"{tmp_manifest.get_codecs().upper()} | {tmp_stream.bit_depth}-bit, {tmp_stream.sample_rate} Hz")
    self.tidal_track_information.track_album_cover.setPixmap(self.load_image_from_web(tmp_track.album.image(160)))

  def load_image_from_web(self, url):
    """Loads the image data from the tidal resources webpage."""
    response = requests.get(url)
    image_data = response.content
    image = QtGui.QPixmap()
    image.loadFromData(image_data)
    return image


class RunningJobsPanel(CustomSidePanel):
  def __init__(self) -> None:
    """Constructor"""
    super().__init__("Running Jobs")


class CompletedJobsPanel(CustomSidePanel):
  def __init__(self) -> None:
    """Constructor"""
    super().__init__("Completed Jobs")


class CustomBottomPanel(QtWidgets.QWidget):
  """Class to create custom bottom panels with."""

  def __init__(self, a_title: str) -> None:
    """Constructor."""
    super().__init__()
    self.btn_close = QtWidgets.QPushButton()
    icons.set_icon(self.btn_close, model_definitions.IconsEnum.CLOSE)
    self.btn_close.setStyleSheet(
      """
      QPushButton {
          background-color: rgba(220, 219, 227, 0.01);
          border: none;
          border-radius: 4px;
          min-width: 36px;
          max-width: 36px;
          min-height: 36px;
          max-height: 36px;
      }
      QPushButton::hover {
          background-color: rgba(220, 219, 227, 0.5);
          border: none;
          min-width: 40px;
          max-width: 40px;
          min-height: 40px;
          max-height: 40px;
      }
      """
    )
    self.lbl_header = QtWidgets.QLabel(a_title)
    self.lbl_header.setStyleSheet(
      """
      QLabel {
        font-size: 20px;
        margin-left: 8px;
      }
      """
    )
    self.layout_header = QtWidgets.QHBoxLayout()
    self.layout_header.addWidget(self.lbl_header)
    self.layout_header.addStretch()
    self.layout_header.addWidget(self.btn_close)

    self.content_frame = QtWidgets.QFrame()
    self.layout_content_frame = QtWidgets.QVBoxLayout()
    self.content_frame.setLayout(self.layout_content_frame)

    self.global_layout = QtWidgets.QVBoxLayout()
    self.global_layout.addLayout(self.layout_header)
    self.global_layout.addWidget(self.content_frame)
    self.setLayout(self.global_layout)
    self.btn_close.clicked.connect(self.hide_panel)

  def add_global_stretch(self):
    """Adds a stretch to the bottom of the global layout."""
    self.global_layout.addStretch()

  def hide_panel(self):
    """Hides the entire panel."""
    self.hide()

  def show_panel(self):
    """Shows the entire panel."""
    self.show()
