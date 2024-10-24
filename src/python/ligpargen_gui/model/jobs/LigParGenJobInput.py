import pathlib

from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.jobs.JobInput import JobInput

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class LigParGenJobInput(JobInput):
  def __init__(self, option: str = "") -> None:
    """
    Constructor.

    Args:
        option (str): Options for the job (-c, -o, -cgen).
    """
    super().__init__()
    self.input_folder: pathlib.Path = pathlib.Path("")  # Add path
    self.option: str = option
    self.output_files: list[str] = []
