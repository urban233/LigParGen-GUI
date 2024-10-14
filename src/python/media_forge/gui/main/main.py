import sys

import requests
from PyQt6 import QtWidgets
from requests import HTTPError

from media_forge.gui.dialog import dialog_login
from media_forge.gui.main import main_frame, main_frame_controller
from media_forge.model import tidal_auth_token
from media_forge.model.util.gui_style import styles_utils

#from media_forge.gui.main import main_frame_controller

# from media_forge.model.util.gui_style import styles_utils
# from media_forge.extension.mv_wrappers.chimerax_wrapper import chimerax_pydd_client
import tidalapi
from tidalapi import Track, Video
from tidalapi.media import StreamManifest


def _download(
        media: Track | Video,
        path_file: str,
) -> str:
  media_name: str = "test"
  urls: [str]

  # Get urls for media.
  if isinstance(media, Track):
    urls = media.get_stream().get_stream_manifest().urls
    stream_manifest: StreamManifest = media.get_stream().get_stream_manifest()

  try:
    # Compute total iterations for progress
    urls_count: int = len(urls)

    if urls_count > 1:
      progress_total: int = urls_count
      block_size: int | None = None
    elif urls_count == 1:
      # Compute progress iterations based on the file size.
      r = requests.get(urls[0], stream=True, timeout=20)

      r.raise_for_status()

      # Get file size and compute progress steps
      total_size_in_bytes: int = int(r.headers.get("content-length", 0))
      block_size: int | None = 1048576
      progress_total: float = total_size_in_bytes / block_size
    else:
      raise ValueError

    # Create progress Task
    # p_task: TaskID = self.progress.add_task(
    #   f"[blue]Item '{media_name[:30]}'",
    #   total=progress_total,
    #   visible=progress_stdout,
    # )

    # Write content to file until progress is finished.
    # while not self.progress.tasks[p_task].finished:
    with open(path_file, "wb") as f:
      for url in urls:
        # Create the request object with stream=True, so the content won't be loaded into memory at once.
        r = requests.get(url, stream=True, timeout=20)

        r.raise_for_status()

        # Write the content to disk. If `chunk_size` is set to `None` the whole file will be written at once.
        for data in r.iter_content(chunk_size=block_size):
          f.write(data)
          # # Advance progress bar.
          # self.progress.advance(p_task)
          #
          # # To send the progress to the GUI, we need to emit the percentage.
          # if not progress_stdout:
          #   self.progress_gui.item.emit(self.progress.tasks[p_task].percentage)
  except HTTPError as e:
    # TODO: Handle Exception...
    pass

  # if isinstance(media, Track) and stream_manifest.is_encrypted:
  #   key, nonce = decrypt_security_token(stream_manifest.encryption_key)
  #   tmp_path_file_decrypted = path_file + "_decrypted"
  #   decrypt_file(path_file, tmp_path_file_decrypted, key, nonce)
  # else:
  #   tmp_path_file_decrypted = path_file

  return path_file


if __name__ == "__main__":
  tmp_refresh_token = False

  app = QtWidgets.QApplication(sys.argv)
  config = tidalapi.Config(quality=tidalapi.Quality.hi_res_lossless)
  session = tidalapi.Session(config)
  # <editor-fold desc="Get fresh Tidal auth token">
  if tmp_refresh_token:
    tmp_login_dialog = dialog_login.DialogLogin(session.pkce_login_url(), "Waiting for user input ...")
    tmp_login_dialog.exec()
    url_redirect = tmp_login_dialog.ui.te_url_redirect.toPlainText()
    session.process_auth_token(session.pkce_get_auth_token(url_redirect))
    tmp_auth_token = tidal_auth_token.TidalAuthToken(
      session.token_type,
      session.access_token,
      session.refresh_token,
      session.expiry_time
    )
    tmp_auth_token.save("tidal_auth.token")
  # </editor-fold>
  else:
    tmp_auth_token = tidal_auth_token.TidalAuthToken.from_stored_token("tidal_auth.token")
    session.load_oauth_session(
      tmp_auth_token.token_type,
      tmp_auth_token.access_token,
      tmp_auth_token.refresh_token,
      tmp_auth_token.expiry_time,
      is_pkce=True
    )

  tmp_main_frame = main_frame.MainFrame(session)
  tmp_main_frame_controller = main_frame_controller.MainFrameController(tmp_main_frame)
  styles_utils.set_stylesheet(app)
  tmp_main_frame_controller.main_frame.show()
  sys.exit(app.exec())
