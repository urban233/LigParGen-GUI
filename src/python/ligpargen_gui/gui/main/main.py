"""Main module containing the entry point for the application."""
import sys
from PyQt6 import QtWidgets
from ligpargen_gui.gui.main import test_frame, main_frame
from ligpargen_gui.model.util.gui_style import styles_utils


if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  tmp_test_frame = test_frame.TestFrame()
  #tmp_test_frame.show()
  tmp_main_frame = main_frame.MainFrame()
  tmp_main_frame.show()
  styles_utils.set_stylesheet(app)
  sys.exit(app.exec())
