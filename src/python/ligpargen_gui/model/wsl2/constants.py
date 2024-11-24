import pathlib


class Paths:
  """Stores important paths."""
  LIGPARGEN_BATCH_FILEPATH: pathlib.Path = pathlib.Path("/home/alma_ligpargen/ligpargen_batch")
  SCRATCH_DIR: pathlib.Path = pathlib.Path("/home/alma_ligpargen/ligpargen_gui/scratch")
  SCRATCH_RESULTS_DIR: pathlib.Path = pathlib.Path("/home/alma_ligpargen/ligpargen_gui/scratch/results")


class JobInputDataKeys:
  """Stores keys to the job dicts."""
  JOB_TYPE = "job_type"
  BOSS_TAR_GZ_FILEPATH = "boss_tar_gz_filepath"
  INPUT_FOLDER = "input_folder"
  OUTPUT_FOLDER = "output_folder"
  OPTIONS = "options"
  OPTIONS_MOLECULE_CHARGE = "molecule_charge"
  OPTIONS_MOL_OPT_ITER = "mol_opt_iter"
  OPTIONS_CHARGE_MODEL = "charge_model"
  OPTIONS_TIMEOUT = "timeout"
  RESULT_FILE_TYPES = "result_file_types"


class JobTypes:
  """Stores the different job types."""
  RUN_LIGPARGEN = "RUN LigParGen"
  INSTALL_BOSS = "INSTALL Boss"
