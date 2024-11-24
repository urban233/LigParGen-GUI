import logging
import pathlib
import re
from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.util import safeguard

logger = default_logging.setup_logger(__file__)


def post_process_tinker_xyz_file(a_filepath: pathlib.Path) -> None:
  """Post processes the TINKER XYZ file.

  Args:
    a_filepath: The filepath of the TINKER XYZ file.
  """
  # <editor-fold desc="Checks">
  safeguard.CHECK(a_filepath is not None)
  safeguard.CHECK(a_filepath.exists())
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
