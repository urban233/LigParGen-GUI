import json
import logging
import pathlib
from typing import Optional

from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util import exception
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class JobInput:
  """Class for a generic job input."""

  def __init__(self, a_job_type: model_definitions.JopTypes) -> None:
    """Constructor."""
    self.job_type: model_definitions.JopTypes = a_job_type

  def _create_json_data(self,) -> dict:
    """Creates the data that can be used for serialization."""
    return {
      "job_type": str(self.job_type)
    }

  def serialize(self, the_instance_attributes: dict) -> str:
    """Serializes the object to a JSON-formatted string."""
    tmp_data = self._create_json_data()
    tmp_data.update(the_instance_attributes)
    return json.dumps(tmp_data, indent=4)

  def serialize_to_file(self, the_instance_attributes: dict, a_filepath: pathlib.Path) -> None:
    """Serializes the object to a JSON-formatted text file.

    Args:
      a_filepath: Path to the output file.

    Raises:
      exception.NoneValueError: If `a_filepath` is None.
    """
    # <editor-fold desc="Checks">
    if a_filepath is None:
      default_logging.append_to_log_file(logger, "a_filepath is None.", logging.ERROR)
      raise exception.NoneValueError("a_filepath is None.")
    # </editor-fold>
    with open(a_filepath, "w") as json_file:
      tmp_data = self._create_json_data()
      tmp_data.update(the_instance_attributes)
      json.dump(tmp_data, json_file, indent=4)
