import glob
import os
import pathlib
import subprocess

from ligpargen_gui.model.util import safeguard


def compare_files(
        a_reference_path: pathlib.Path,
        a_to_compare_path: pathlib.Path,
        a_report_path: pathlib.Path,
        a_file_extension: str,
        a_result_type: str
) -> None:
  """Compares the files of two directories.

  Args:
    a_reference_path: The path to the reference files
    a_to_compare_path: The path to the comparison files
    a_report_path: The path to store the report files
    a_file_extension: The extension of the files to compare
    a_result_type: The type of results to compare
  """
  # <editor-fold desc="Checks">
  safeguard.CHECK(a_reference_path is not None)
  safeguard.CHECK(a_reference_path.exists())
  safeguard.CHECK(a_to_compare_path is not None)
  safeguard.CHECK(a_to_compare_path.exists())
  safeguard.CHECK(a_report_path is not None)
  safeguard.CHECK(a_report_path.exists())
  safeguard.CHECK(a_file_extension is not None)
  safeguard.ENSURE(a_file_extension != "")
  safeguard.CHECK(a_result_type is not None)
  safeguard.ENSURE(a_result_type != "")
  # </editor-fold>
  tmp_reference_filepaths = {}
  tmp_to_compare_filepaths = {}

  for tmp_reference_file in glob.glob(os.path.join(a_reference_path, f'*.{a_file_extension}')):
    filename = os.path.basename(tmp_reference_file)
    base_name = filename.replace(a_result_type, '')
    tmp_reference_filepaths[base_name] = tmp_reference_file

  for tmp_to_compare_file in glob.glob(os.path.join(a_to_compare_path, f'*.{a_file_extension}')):
    filename = os.path.basename(tmp_to_compare_file)
    base_name = filename.replace(a_result_type, '')
    tmp_to_compare_filepaths[base_name] = tmp_to_compare_file

  for base_name in tmp_reference_filepaths:
    if base_name in tmp_to_compare_filepaths.keys():
      print(f"Running compare of: {tmp_reference_filepaths[base_name]} vs {tmp_to_compare_filepaths[base_name]}")
      subprocess.run(
        [
          "powershell.exe",
          ".\\external\\WinMerge\\WinMergeU.exe",
          str(tmp_reference_filepaths[base_name]),
          str(tmp_to_compare_filepaths[base_name]),
          "/noninteractive",
          "/minimize",
          "/u",
          "/or",
          str(os.path.join(a_report_path, f"{base_name.replace('.', '_')}_report.html"))
        ]
      )
