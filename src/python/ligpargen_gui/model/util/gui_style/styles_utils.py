"""Module for all styles related functions."""
import logging
import os
import pathlib
from PyQt6 import QtWidgets
from ligpargen_gui.model.custom_logging import default_logging
# from ligpargen_gui.model.util import exception
from ligpargen_gui.model.preference import model_definitions

__docformat__ = "google"

from ligpargen_gui.model.util import exception, safeguard

logger = default_logging.setup_logger(__file__)


def set_stylesheet(self) -> None:
  """Sets the style sheet to the QMainWindow or a QDialog.

  Args:
    self: a QMainWindow or QDialog
  """
  # <editor-fold desc="Checks">
  safeguard.CHECK(self is not None)
  # </editor-fold>
  with open(
          pathlib.Path(
            f"{model_definitions.ModelDefinitions.PROGRAM_SRC_PATH}/python/ligpargen_gui/model/util/gui_style/style.css"
          ),
          "r",
          encoding="utf-8",
  ) as file:
    style = file.read()
    # Set the stylesheet of the application
    self.setStyleSheet(style)


def set_default_button_style(a_button: QtWidgets.QPushButton) -> None:
  """Sets the default button style.

  Args:
    a_button: The button to set the default style for.
  """
  # <editor-fold desc="Checks">
  safeguard.CHECK(a_button is not None)
  # </editor-fold>
  a_button.setStyleSheet(
    """
      QPushButton {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }

    QPushButton:disabled {
        background-color: #fff;
        color: #B0B0B0;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }

    QPushButton::pressed {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 2px;
        border-radius: 4px;
        border-color: #367AF6;
        padding: 0px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }
    """)
