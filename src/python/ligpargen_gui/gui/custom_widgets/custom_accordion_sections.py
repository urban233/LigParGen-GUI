from typing import Callable, Union

import tidalapi
from PyQt6 import QtWidgets

from media_forge.gui.dialog import dialog_storage_variables
from media_forge.model.qmodel import search_model


class SearchTableTidal(QtWidgets.QWidget):
  """Class for displaying search results of a tidal query in a table format."""

  def __init__(self, a_model, a_tidal_session, parent=None) -> None:
    """Constructor."""
    super().__init__(parent)
    self.model = a_model
    self.tidal_session = a_tidal_session

    self.search_tracks_main_layout = QtWidgets.QVBoxLayout()
    self.setLayout(self.search_tracks_main_layout)

    self.btn_search = QtWidgets.QPushButton("Search")
    self.txt_search = QtWidgets.QLineEdit()
    self.layout_search = QtWidgets.QHBoxLayout()
    self.layout_search.addWidget(self.txt_search)
    self.layout_search.addWidget(self.btn_search)
    self.search_tracks_main_layout.addLayout(self.layout_search)

    self.search_tracks_table_view = QtWidgets.QTableView()
    self.search_tracks_table_view.setFixedHeight(300)
    self.search_tracks_table_view.setModel(self.model)
    self.search_tracks_main_layout.addWidget(self.search_tracks_table_view)

    self.btn_manage_variables = QtWidgets.QPushButton("Manage variables")
    self.layout_add_to_job = QtWidgets.QHBoxLayout()
    self.layout_add_to_job.addStretch()
    self.layout_add_to_job.addWidget(self.btn_manage_variables)
    self.search_tracks_main_layout.addLayout(self.layout_add_to_job)

    self.btn_add_to_job = QtWidgets.QPushButton("Add to job")
    self.layout_add_to_job = QtWidgets.QHBoxLayout()
    self.layout_add_to_job.addStretch()
    self.layout_add_to_job.addWidget(self.btn_add_to_job)
    self.search_tracks_main_layout.addLayout(self.layout_add_to_job)

    self.btn_search.clicked.connect(self._search)
    # self.btn_add_to_job.clicked.connect(self._open_storage_variables_test)
    #self.btn_manage_variables.clicked.connect(self._open_storage_variables)

  def connect_search_tracks_table_view_clicked(self, a_callable: Callable):
    """Connects the clicked signal of the table view with the given callable."""
    self.search_tracks_table_view.clicked.connect(a_callable)

  def _search(self):
    """Search for entered query."""
    tmp_search_result: dict[
      str, Union[
        list[tidalapi.artist.Artist],
        list[tidalapi.album.Album],
        list[tidalapi.media.Track],
        list[tidalapi.media.Video],
        list[tidalapi.playlist.Playlist]]
    ] = self.tidal_session.search(self.txt_search.text())
    tmp_tracks: list[tidalapi.media.Track] = tmp_search_result["tracks"]
    self.search_model = search_model.SearchModel.from_a_list_of_tracks(tmp_tracks)
    self.search_tracks_table_view.setModel(self.search_model)


class TrackInformationTidal(QtWidgets.QWidget):
  """Class for representing the information of a given track"""

  def __init__(self) -> None:
    """Constructor."""
    super().__init__()
    self.main_layout = QtWidgets.QVBoxLayout()
    self.setLayout(self.main_layout)
  
    self.track_title = QtWidgets.QLabel("Generic Title")
    self.track_title.setStyleSheet("""QLabel {font-size: 13px; font-weight: bold;}""")
    self.track_album_artist = QtWidgets.QLabel("Generic Album Artist")
    self.track_album_name = QtWidgets.QLabel("Generic Album Name")
    self.album_release_date = QtWidgets.QLabel("01-01-2024")
    self.track_audio_quality = QtWidgets.QLabel("FLAC | 16/44.1 kHz | 1054k")
    self.layout_track_infos = QtWidgets.QVBoxLayout()
    self.layout_track_infos.addWidget(self.track_title)
    self.layout_track_infos.addWidget(self.track_album_artist)
    self.layout_track_infos.addWidget(self.track_album_name)
    self.layout_track_infos.addWidget(self.album_release_date)
    self.layout_track_infos.addWidget(self.track_audio_quality)
    self.layout_track_infos.addStretch()
  
    self.track_album_cover = QtWidgets.QLabel("Album Cover")
    self.track_album_cover.setFixedSize(160, 160)
  
    self.track_info_layout = QtWidgets.QHBoxLayout()
    self.track_info_layout.addWidget(self.track_album_cover)
    self.track_info_layout.addLayout(self.layout_track_infos)
    self.main_layout.addLayout(self.track_info_layout)


class JobTableTidal(QtWidgets.QWidget):
  """Class for displaying chosen tracks."""

  def __init__(self, a_model, a_tidal_session, parent=None) -> None:
    """Constructor."""
    super().__init__(parent)
    self.model = a_model
    self.tidal_session = a_tidal_session

    self.job_information_main_layout = QtWidgets.QVBoxLayout()
    self.setLayout(self.job_information_main_layout)

    self.tracks_to_job_table_view = QtWidgets.QTableView()
    self.tracks_to_job_table_view.setFixedHeight(300)
    self.tracks_to_job_table_view.setModel(self.model)
    self.job_information_main_layout.addWidget(self.tracks_to_job_table_view)

    self.btn_add_to_job = QtWidgets.QPushButton("Start job")
    self.layout_add_to_job = QtWidgets.QHBoxLayout()
    self.layout_add_to_job.addStretch()
    self.layout_add_to_job.addWidget(self.btn_add_to_job)
    self.job_information_main_layout.addLayout(self.layout_add_to_job)

  def connect_tracks_to_job_table_view_clicked(self, a_callable: Callable):
    """Connects the clicked signal of the table view with the given callable."""
    self.tracks_to_job_table_view.clicked.connect(a_callable)

  def _search(self):
    """Search for entered query."""
    tmp_search_result: dict[
      str, Union[
        list[tidalapi.artist.Artist],
        list[tidalapi.album.Album],
        list[tidalapi.media.Track],
        list[tidalapi.media.Video],
        list[tidalapi.playlist.Playlist]]
    ] = self.tidal_session.search(self.txt_search.text())
    tmp_tracks: list[tidalapi.media.Track] = tmp_search_result["tracks"]
    self.search_model = search_model.SearchModel.from_a_list_of_tracks(tmp_tracks)
    self.tracks_to_job_table_view.setModel(self.search_model)
