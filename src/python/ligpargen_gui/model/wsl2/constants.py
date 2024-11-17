import pathlib


class Paths:
  LIGPARGEN_BATCH_FILEPATH: pathlib.Path = pathlib.Path("/home/alma_ligpargen/ligpargen_batch")
  SCRATCH_DIR: pathlib.Path = pathlib.Path("/home/alma_ligpargen/ligpargen_gui/scratch")
  SCRATCH_RESULTS_DIR: pathlib.Path = pathlib.Path("/home/alma_ligpargen/ligpargen_gui/scratch/results")


class JobInputDataKeys:
  JOB_TYPE = "job_type"
  BOSS_TAR_GZ_FILEPATH = "boss_tar_gz_filepath"
  INPUT_FOLDER = "input_folder"
  OUTPUT_FOLDER = "output_folder"
  OPTIONS = "options"
  OPTIONS_MOLECULE_CHARGE = "molecule_charge"
  OPTIONS_MOL_OPT_ITER = "mol_opt_iter"
  OPTIONS_CHARGE_MODEL = "charge_model"
  OPTIONS_TIMEOUT = "timeout"
  RESULT_FILE_TYPES = "result_file_types"  # Unsure if this is the right key, might be wrong and needs to be checked!!


class JobTypes:
  RUN_LIGPARGEN = "RUN LigParGen"
  INSTALL_BOSS = "INSTALL Boss"
