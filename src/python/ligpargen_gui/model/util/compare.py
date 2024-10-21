import glob
import os
import pathlib
import subprocess


def compare_files(
        a_reference_path: pathlib.Path,
        a_to_compare_path: pathlib.Path,
        a_report_path: pathlib.Path,
        a_file_extension: str,
        a_result_type: str
):
  """Compares the files of two directories."""
  # TODO: Add argument checks & expand doc string
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
