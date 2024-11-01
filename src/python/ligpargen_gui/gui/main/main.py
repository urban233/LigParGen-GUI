"""Main module containing the entry point for the application."""
import sys
from PyQt6 import QtWidgets
from ligpargen_gui.gui.main import main_frame, main_frame_controller
from ligpargen_gui.model.util import filesystem_util
from ligpargen_gui.model.util.gui_style import styles_utils, icons


if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  tmp_boss_is_installed = filesystem_util.check_file_exists_in_wsl(
    "alma9LigParGen0205", "/home/alma_ligpargen/boss/BOSS"  # TODO: Change distro name!!!
  )
  if not tmp_boss_is_installed:
    # TODO: Add dialog window to install BOSS
    print("Boss is not installed!")
  else:
    tmp_main_frame = main_frame.MainFrame()
    tmp_main_frame_controller = main_frame_controller.MainFrameController(tmp_main_frame)
    tmp_main_frame_controller.main_frame.show()
    styles_utils.set_stylesheet(app)
    sys.exit(app.exec())
