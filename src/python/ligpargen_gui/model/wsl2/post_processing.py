import logging
import pathlib
import re

from wsl2 import default_logging, exception

logger = default_logging.setup_logger(__file__)


def post_process_tinker_xyz_file(a_filepath: pathlib.Path):
  """Post processes the TINKER XYZ file.

  Args:
    a_filepath: The filepath of the TINKER XYZ file.

  Raises:
    exception.NoneValueError: If `a_filepath` is None.
    exception.IllegalArgumentError: If `a_filepath` does not exist.
  """
  # <editor-fold desc="Checks">
  if a_filepath is None:
    default_logging.append_to_log_file(logger, "a_filepath is None.", logging.ERROR)
    raise exception.NoneValueError("a_filepath is None.")
  if a_filepath == "":
    default_logging.append_to_log_file(logger, "a_filepath does not exist.", logging.ERROR)
    raise exception.IllegalArgumentError("a_filepath does not exist.")
  # </editor-fold>
  with open(a_filepath, 'r') as file:
    lines = file.readlines()
  processed_lines = []
  for i, line in enumerate(lines):
    if i == 0:
      # Adds the filename (without extension) after the first value of the first line
      first_value = line.strip().split()[0]
      tmp_filename_without_extension = a_filepath.name.replace(".tinker.xyz", "")
      modified_line = f"    {first_value} {tmp_filename_without_extension}\n"
    else:
      # Removes numbers after element symbols, for all other lines
      modified_line = re.sub(r'\b([A-Z][a-z]?)[0-9]+\b', r'\1', line)
    processed_lines.append(modified_line)

  with open(a_filepath, 'w') as file:
    file.writelines(processed_lines)
