import json
import logging
import pathlib

from ligpargen_gui.model.data_classes import ligpargen_options
from ligpargen_gui.model.jobs.job_input import JobInput
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class LigParGenJobInput(JobInput):
  """Class that defines the input for a LigParGen job."""

  def __init__(self,
               an_input_folder: pathlib.Path,
               an_output_folder: pathlib.Path,
               the_options: "ligpargen_options.LigParGenOptions",
               the_result_file_types: list["model_definitions.LigParGenResultFileTypes"]) -> None:
    """Constructor.

    Args:
      an_input_folder: Path to the input folder.
      an_output_folder: Path to the output folder.
      the_options: Option for the job (-c, -o, -cgen).
      the_result_file_types: File types for the job.

    Raises:
      exception.NoneValueError: If any of the arguments are None.
      exception.IllegalArgumentError: If `the_input_folder` does not exist or `the_result_file_types` is an empty list.
    """
    # <editor-fold desc="Checks">
    if an_input_folder is None:
      default_logging.append_to_log_file(logger, "an_input_folder is None.", logging.ERROR)
      raise exception.NoneValueError("an_input_folder is None.")
    if not an_input_folder.exists():
      default_logging.append_to_log_file(logger, "an_input_folder does not exist.", logging.ERROR)
      raise exception.IllegalArgumentError("an_input_folder does not exist.")
    if an_output_folder is None:
      default_logging.append_to_log_file(logger, "an_output_folder is None.", logging.ERROR)
      raise exception.NoneValueError("an_output_folder is None.")
    if the_options is None:
      default_logging.append_to_log_file(logger, "the_options is None.", logging.ERROR)
      raise exception.NoneValueError("the_options is None.")
    if the_result_file_types is None:
      default_logging.append_to_log_file(logger, "the_result_file_types is None.", logging.ERROR)
      raise exception.NoneValueError("the_result_file_types is None.")
    if len(the_result_file_types) == 0:
      default_logging.append_to_log_file(logger, "the_result_file_types is an empty list.", logging.ERROR)
      raise exception.IllegalArgumentError("the_result_file_types is an empty list.")
    # </editor-fold>
    super().__init__(a_job_type=model_definitions.JopTypes.RUN_LIGPARGEN)
    # <editor-fold desc="Instance attributes">
    self.input_folder: pathlib.Path = an_input_folder
    """Represents the folder where all input files are."""
    self.output_folder: pathlib.Path = an_output_folder
    """Represents the folder where all selected results will be stored."""
    self.options: "ligpargen_options.LigParGenOptions" = the_options
    """Contains all possible LigParGen CLI tool options that are also available on the web server."""
    self.result_file_types: list["model_definitions.LigParGenResultFileTypes"] = the_result_file_types
    """Contains all selected result file types."""
    # </editor-fold>

  def get_obj_as_dict(self):
    """Gets all instance attributes as dict."""
    return {
      "input_folder": str(self.input_folder),
      "output_folder": str(self.output_folder),
      "options": self.options.__dict__,
      "result_file_types": self.result_file_types
    }
