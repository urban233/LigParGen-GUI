import logging
from dataclasses import dataclass

from ligpargen_gui.model.custom_logging import default_logging
from ligpargen_gui.model.util import exception, safeguard

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


@dataclass
class LigParGenOptions:
  """Dataclass for storing all options related to LigParGen."""
  # <editor-fold desc="Class attributes">
  mol_opt_iter: int
  """Represents the iteration number of the molecular optimization."""
  charge_model: str
  """Represents the name of the charge model."""
  molecule_charge: int
  """Represents the charge of the molecule."""
  timeout: int
  """Represents the timeout used for the LigParGen CLI tool."""
  # </editor-fold>

  def __init__(self, a_mol_opt_iter: int, a_charge_model: str, a_molecule_charge: int, a_timeout: int):
    # <editor-fold desc="Checks">
    safeguard.CHECK(a_mol_opt_iter is not None)
    safeguard.CHECK(0 <= a_mol_opt_iter <= 3)
    safeguard.CHECK(a_charge_model is not None)
    safeguard.CHECK(a_charge_model == "CM1A-LBCC" or a_charge_model == "CM1A")
    safeguard.CHECK(a_molecule_charge is not None)
    safeguard.CHECK(-2 <= a_molecule_charge <= 2)
    safeguard.ENSURE(a_timeout > 0)
    # </editor-fold>
    self.mol_opt_iter = a_mol_opt_iter
    self.charge_model = a_charge_model
    self.molecule_charge = a_molecule_charge
    self.timeout = a_timeout
