import logging
from dataclasses import dataclass

from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.util import exception

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


@dataclass
class LigParGenOptions:
  # <editor-fold desc="Class attributes">
  mol_opt_iter: int
  """Represents the iteration number of the molecular optimization."""
  charge_model: str
  """Represents the name of the charge model."""
  molecule_charge: int
  """Represents the charge of the molecule."""
  # </editor-fold>

  def __init__(self, a_mol_opt_iter: int, a_charge_model: str, a_molecule_charge: int):
    # <editor-fold desc="Checks">
    if a_mol_opt_iter is None:
      default_logging.append_to_log_file(logger, "a_mol_opt_iter is None.", logging.ERROR)
      raise exception.NoneValueError("a_mol_opt_iter is None.")
    if a_mol_opt_iter < 0 or a_mol_opt_iter > 3:
      default_logging.append_to_log_file(logger, "a_mol_opt_iter is less than 0 or above 3.", logging.ERROR)
      raise exception.IllegalArgumentError("a_mol_opt_iter is less than 0 or above 3.")
    if a_charge_model is None:
      default_logging.append_to_log_file(logger, "a_charge_model is None.", logging.ERROR)
      raise exception.NoneValueError("a_charge_model is None.")
    if a_charge_model != "CM1A-LBCC" and a_charge_model != "CM1A":
      default_logging.append_to_log_file(logger, "a_charge_model is invalid.", logging.ERROR)
      raise exception.IllegalArgumentError("a_charge_model is invalid.")
    if a_molecule_charge is None:
      default_logging.append_to_log_file(logger, "a_molecule_charge is None.", logging.ERROR)
      raise exception.NoneValueError("a_molecule_charge is None.")
    if a_molecule_charge < -2 or a_molecule_charge > 2:
      default_logging.append_to_log_file(logger, "a_molecule_charge is less than -2 or above 2.", logging.ERROR)
      raise exception.IllegalArgumentError("a_molecule_charge is less than -2 or above 2.")
    # </editor-fold>
    self.mol_opt_iter = a_mol_opt_iter
    self.charge_model = a_charge_model
    self.molecule_charge = a_molecule_charge
