import pathlib

from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.data_classes import ligpargen_options
from ligpargen_gui.model.jobs.job_input import JobInput
from ligpargen_gui.model.preference import model_definitions

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class LigParGenJobInput(JobInput):
  def __init__(self, an_input_folder: pathlib.Path,
               the_options: "ligpargen_options.LigParGenOptions",
               the_result_file_types: list["model_definitions.LigParGenResultFileTypes"]) -> None:
    """Constructor.

    Args:
      an_input_folder: Path to the input folder.
      the_options: Option for the job (-c, -o, -cgen).
      the_result_file_types: File types for the job.
    """
    super().__init__()
    self.input_folder: pathlib.Path = an_input_folder
    self.options: "ligpargen_options.LigParGenOptions" = the_options
    self.result_file_types: list["model_definitions.LigParGenResultFileTypes"] = the_result_file_types
