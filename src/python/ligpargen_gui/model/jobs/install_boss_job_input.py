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


class InstallBossJobInput(JobInput):
  """Class that defines the input for an 'install boss' job."""

  def __init__(self, the_boss_tar_gz_filepath: pathlib.Path) -> None:
    """Constructor.

    Args:
      the_boss_tar_gz_filepath: Filepath to the boss.tar.gz file.

    Raises:
      exception.NoneValueError: If `the_boss_tar_gz_filepath` is None.
      exception.IllegalArgumentError: If `the_boss_tar_gz_filepath` does not exist.
    """
    # <editor-fold desc="Checks">
    if the_boss_tar_gz_filepath is None:
      default_logging.append_to_log_file(logger, "the_boss_tar_gz_filepath is None.", logging.ERROR)
      raise exception.NoneValueError("the_boss_tar_gz_filepath is None.")
    if not the_boss_tar_gz_filepath.exists():
      default_logging.append_to_log_file(logger, "the_boss_tar_gz_filepath does not exist.", logging.ERROR)
      raise exception.IllegalArgumentError("the_boss_tar_gz_filepath does not exist.")
    # </editor-fold>
    super().__init__(a_job_type=model_definitions.JopTypes.INSTALL_BOSS)
    # <editor-fold desc="Instance attributes">
    self.boss_tar_gz_filepath: pathlib.Path = the_boss_tar_gz_filepath
    """Represents the filepath to the boss.tar.gz file."""
    # </editor-fold>

  def get_obj_as_dict(self):
    """Gets all instance attributes as dict."""
    return {"boss_tar_gz_filepath": str(self.boss_tar_gz_filepath)}
