import pathlib

from ligpargen_gui.gui.util import gui_util
from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.util import exception

logger = default_logging.setup_logger(__file__)


def validate_path(the_current_entered_text: str) -> tuple[bool, str, str]:
  """Validates the input for a valid path.

  Args:
      the_current_entered_text (str): The text entered for the sequence name.

  Returns:
      A tuple containing a boolean indicating whether the input is valid and a string representing
      an error message if applicable and a stylesheet for a line edit.

  Raises:
      exception.IllegalArgumentError: If either `the_current_entered_text` or `the_current_sequences` is None.
      exception.NotMainThreadError: If function is called not from the main thread.
  """
  # <editor-fold desc="Checks">
  if the_current_entered_text is None:
    logger.error('the_current_entered_text is None.')
    raise exception.IllegalArgumentError('the_current_entered_text is None.')
  if not gui_util.is_main_thread():
    raise exception.NotMainThreadError()

  # </editor-fold>

  allowed_chars = {
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
    '-',
    '_',
    '\\',
    ':'
  }
  for char in the_current_entered_text:
    if char not in allowed_chars:
      return False, 'Invalid character!', """QLineEdit {color: #ba1a1a; border-color: #ba1a1a;}"""
  if the_current_entered_text == '':
    return False, 'Please enter a valid path!', """QLineEdit {color: #ba1a1a; border-color: #ba1a1a;}"""
  if not pathlib.Path(the_current_entered_text).exists():
    return False, 'Path could not be found!', """QLineEdit {color: #ba1a1a; border-color: #ba1a1a;}"""
  return True, '', """QLineEdit {color: #000000; border-color: #DCDBE3;}"""
