import inspect
import logging

from wsl2 import default_logging

logger = default_logging.setup_logger(__file__)


def ENSURE(expr) -> None:
  """Ensures that a condition (expr) is True. If False, the program crashes
  with a detailed error message including the file and line number.

  Args:
    expr (bool): The condition to evaluate.
  """
  if not expr:
    # Get file name and line number of the caller
    frame = inspect.currentframe().f_back
    file_name = frame.f_code.co_filename
    line_number = frame.f_lineno

    # Construct a detailed assertion message
    message = f"CHECK failed: {expr}, in file {file_name}, line {line_number}"
    default_logging.append_to_log_file(logger, message, logging.ERROR)


def ENSURE_RETURN(expr, return_code: int) -> int:
    """Ensures that a condition (expr) is True. If False, the program crashes
    with a detailed error message including the file and line number.

    Args:
      expr (bool): The condition to evaluate.
      return_code (int): The return code.
    Returns:
      An error code.
    """
    if not expr:
      # Get file name and line number of the caller
      frame = inspect.currentframe().f_back
      file_name = frame.f_code.co_filename
      line_number = frame.f_lineno
      # Construct a detailed assertion message
      message = f"CHECK failed: {expr}, in file {file_name}, line {line_number}"
      default_logging.append_to_log_file(logger, message, logging.ERROR)
      return return_code
    return 0
