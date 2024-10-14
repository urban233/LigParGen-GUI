import datetime
import enum
import os
import pathlib


class ModelDefinitions:
  """Global basic definitions for the core component.

  Should be used as singleton class!
  """
  PROGRAM_ROOT_PATH = pathlib.Path(__file__).parent.parent.parent.parent.parent.parent
  PROGRAM_BIN_ROOT_PATH = "C:\\ProgramData\\mediaforge\\MediaForge\\bin\\MediaForge"
  """Path to the root of the program."""
  PROGRAM_SRC_PATH = pathlib.Path(
    __file__).parent.parent.parent.parent.parent  # TODO: Must be switched to if ready for first tests f"{PROGRAM_BIN_ROOT_PATH}\\src"
  """Path to the root of the program sources."""
  print(PROGRAM_SRC_PATH)
  DEFAULT_WORKSPACE_PATH: pathlib.Path = pathlib.Path(
    f"{os.path.expanduser('~')}/.mediaforge/default"
  )
  """Default workspace path"""
  SETTINGS_FILENAME = 'settings.json'
  """Default settings filename"""
  DEFAULT_SETTINGS_PATH: pathlib.Path = pathlib.Path(
    f"{os.path.expanduser('~')}/.mediaforge/"
  )
  DEFAULT_SETTINGS_FILEPATH: pathlib.Path = pathlib.Path(
    f"{os.path.expanduser('~')}/.mediaforge/{SETTINGS_FILENAME}"
  )
  """Default settings path"""
  DEFAULT_LOG_PATH: pathlib.Path = pathlib.Path(f'{DEFAULT_SETTINGS_PATH}/logs')
  """Default logging path"""
  LOG_FILENAME = f'{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d}_{datetime.datetime.now().hour:02d}-{datetime.datetime.now().minute:02d}.log'  # noqa: E501
  """Log filename"""
  LOG_FILEPATH = pathlib.Path(f'{DEFAULT_SETTINGS_PATH}/logs/{LOG_FILENAME}')
  """Complete log filepath"""
  ASSETS_PATH = pathlib.Path(f"{PROGRAM_ROOT_PATH}/assets")
  """Path to the assets folder"""
  ICONS_PATH = pathlib.Path(f"{ASSETS_PATH}/icons")
  print(ICONS_PATH)
  """Path to the icons folder"""
  STATUS_MESSAGE_TIMEOUT = 5000  # value in msec
  """The standard status bar message timeout"""

# <editor-fold desc="Model roles">
class RolesEnum(enum.IntEnum):
  """Enumeration for storing possible model roles."""
  OBJECT_ROLE = 1003
  """Model role to store an object."""
  TYPE_ROLE = 1004
  """Model role to store a type."""
  FILEPATH_ROLE = 1005
  """Model role to store a filepath."""
  CHAIN_COLOR_ROLE = 1006
  """Model role to store a chain color."""
# </editor-fold>


# <editor-fold desc="Model types">
class TypesEnum(enum.StrEnum):
  """Enumeration for storing possible model types."""
  PROJECT_TYPE = "project"
  """Model type for storing a project."""
  SEQUENCE_TYPE = "sequence"
  """Model type for storing a sequence."""
  TRACK_TYPE = "track"
  """Model type for storing a track."""
  CHAIN_TYPE = "chain"
  """Model type for storing a chain."""
  RESIDUE_TYPE = "residue"
  """Model type for storing a residue."""
  ATOM_TYPE = "atom"
  """Model type for storing an atom."""
  LIGAND_TYPE = "ligand"
  """Model type for storing an ligand."""
# </editor-fold>


class StorageSpaceType(enum.StrEnum):
  """Enumeration for storing possible storage spaces"""
  MUSIC = "Music"
  VIDEO = "Video"
  IMAGE = "Image"


class StorageVariableType(enum.StrEnum):
  """Enumeration for storing possible storage variables"""
  USER = "User"
  HI_RES = "HiRes"
  CD_QUALITY = "CD-Quality"
  MP3 = "MP3"


class ComponentsEnum(enum.IntEnum):
  """Enumeration for storing all components."""
  CREATE_PROJECT = 1001
  OPEN_PROJECT = 1002

  IMPORT_SEQUENCE = 1101
  IMPORT_PROTEIN = 1201
  IMPORT_LIGAND = 1301


class IconsEnum(enum.StrEnum):
  """Class for storing the icon filenames with their usage name."""
  HELP = "HELP"
  ADD_SEQUENCE = "NOTE_ADD"
  ADD_SEQUENCE_DISABLED = "NOTE_ADD_DISABLED"
  IMPORT_SEQUENCE = "UPLOAD_FILE"
  IMPORT_SEQUENCE_DISABLED = "UPLOAD_FILE_DISABLED"
  SAVE_SEQUENCE = "FILE_SAVE"
  SAVE_SEQUENCE_DISABLED = "FILE_SAVE_DISABLED"
  DELETE_SEQUENCE = "SCAN_DELETE"
  DELETE_SEQUENCE_DISABLED = "SCAN_DELETE_DISABLED"
  EXPAND_ALL = "EXPAND_ALL"
  COLLAPSE_ALL = "COLLAPSE_ALL"
  IMPORT_PROTEIN = "UPLOAD_FILE"
  IMPORT_PROTEIN_DISABLED = "UPLOAD_FILE_DISABLED"
  SAVE_PROTEIN = "FILE_SAVE"
  SAVE_PROTEIN_DISABLED = "FILE_SAVE_DISABLED"
  DELETE_PROTEIN = "SCAN_DELETE"
  DELETE_PROTEIN_DISABLED = "SCAN_DELETE_DISABLED"
  OPEN_SESSION = "OPEN_IN_NEW"
  OPEN_SESSION_DISABLED = "OPEN_IN_NEW_DISABLED"
  CREATE_SESSION_SCENE = "ADD_CIRCLE"
  CREATE_SESSION_SCENE_DISABLED = "ADD_CIRCLE_DISABLED"
  UPDATE_SESSION_SCENE = "CHANGE_CIRCLE"
  UPDATE_SESSION_SCENE_DISABLED = "CHANGE_CIRCLE_DISABLED"
  DELETE_SESSION_SCENE = "CANCEL"
  DELETE_SESSION_SCENE_DISABLED = "CANCEL_DISABLED"
  DELETE_PROTEIN_PAIR = "SCAN_DELETE"
  DELETE_PROTEIN_PAIR_DISABLED = "SCAN_DELETE_DISABLED"
  JOBS = "PLAY_CIRCLE"
  JOBS_RUNNING = "PLAY_CIRCLE_RUN"
  NOTIFY = "NOTIFICATIONS"
  NOTIFY_UNREAD = "NOTIFICATIONS_UNREAD"
  NEW = "DRAFT"
  OPEN = "FOLDER_OPEN"
  EXPORT = "SHARE_WINDOWS"
  IMPORT = "BROWSER_UPDATED"
  CLOSE = "CLOSE"
  DELETE = "DELETE"
  BACK = "ARROW_BACK"
  DISTANCE_ANALYSIS = "ANGSTROM_DISTANCE"
  CARTOON_REPR = "CARTOON_REPR"
  STICKS_REPR = "STICKS_REPR"
  RIBBON_REPR = "RIBBON_REPR"
  SPHERES_REPR = "SPHERES_REPR"
  LINES_REPR = "LINES_REPR"
  DOTS_REPR = "DOTS_REPR"
  MESH_REPR = "MESH_REPR"
  SURFACE_REPR = "SURFACE_REPR"
  MORE = "MORE_VERT"
  COLOR_GRID = "GRID_VIEW"
  IMAGE = "IMAGE"
  RAY_TRACED_IMAGE = "PHOTO_FRAME"
  EDIT = "EDIT"
  MONOMER_PROTEIN = "MONOMER_PROTEIN"
  MULTIMER_PROTEIN = "MULTIMER_PROTEIN"
  DOCKING = "DOCKING"
  RIBBON_PANEL_SETTINGS = "OPEN_IN_NEW_DOWN"
  HOME = "HOME"
  TREE_EXPAND = "KEYBOARD_ARROW_RIGHT"
  TREE_COLLAPSE = "KEYBOARD_ARROW_DOWN"
  MUSIC_NOTE = "MUSIC_NOTE"
  ALBUM = "ALBUM"
  ARTIST = "ARTIST"
  CANCEL = "DO_NOT_DISTURB_ON"
  TIDAL = "TIDAL"
  YOUTUBE = "YOUTUBE"
  TRANSFER = "SYNC_ALT"
  CONVERT = "RULE_SETTINGS"


class JobStatus(enum.Enum):
  """An enum for all job progress states."""
  QUEUED = "queued"
  WAITING = "waiting"
  RUNNING = "running"
  FINISHED = "finished"
  FAILED = "failed"


class JobType(enum.StrEnum):
  """An enum for all job types."""
  PREDICTION = "structure prediction"
  DISTANCE_ANALYSIS = "distance analysis"
  PREDICTION_AND_DISTANCE_ANALYSIS = "prediction and distance analysis"
  RAY_TRACING = "ray-tracing"
  GENERAL_PURPOSE = "general-purpose"
  ABORT = "abort"


class JobDescriptionKeys(enum.StrEnum):
  """An enum for all job description keys.

  Notes:
      IMPORTANT: always use the .value of the enum! Otherwise, the connection to the auxiliary pymol would fail!
  """
  JOB_TYPE = "job_type"
  # Prediction keys
  PDB_FILEPATH = "pdb_filepath"
  # Distance analysis keys
  PROTEIN_PAIR_NAME = "the_protein_pair_name"
  PROTEIN_1_PDB_CACHE_FILEPATH = "a_protein_1_pdb_cache_filepath"
  PROTEIN_2_PDB_CACHE_FILEPATH = "a_protein_2_pdb_cache_filepath"
  PROTEIN_1_PYMOL_SELECTION_STRING = "a_protein_1_pymol_selection_string"
  PROTEIN_2_PYMOL_SELECTION_STRING = "a_protein_2_pymol_selection_string"
  CUTOFF = "a_cutoff"
  CYCLES = "the_cycles"
  # Ray-tracing keys
  IMAGE_DESTINATION_FILEPATH = "dest"
  CACHED_SESSION_FILEPATH = "cached"
  RAY_TRACE_MODE = "mode"
  RAY_TEXTURE = "texture"
  RAY_TRACING_RENDERER = "renderer"
  # General purpose
  JOB_SHORT_DESCRIPTION = "job_short_description"
  PYMOL_SESSION = "pymol_session"
  PROTEIN_NAME = "protein_name"


class JobShortDescription(enum.StrEnum):
  """An enum for all job short descriptions.

  Notes:
      IMPORTANT: always use the .value of the enum! Otherwise, the connection to the auxiliary pymol would fail!
  """
  RUN_STRUCTURE_PREDICTION = "Run ColabFold structure prediction."
  RUN_DISTANCE_ANALYSIS = "Run distance analysis."
  CREATE_RAY_TRACED_IMAGE = "Create new ray traced image."
  CREATE_NEW_PROTEIN_PYMOL_SESSION = "Create new protein pymol session."
  GET_ALL_CHAINS_OF_GIVEN_PROTEIN = "Get all chains of a given protein."
  GET_ALL_SCENES_OF_SESSION = "Get all scenes of a given pymol session."
  CONSOLIDATE_MOLECULE_OBJECT_TO_FIRST_STATE = (
    "Consolidate molecule object to first state."
  )
  CLEAN_PROTEIN_UPDATE_STRUCTURE = "Clean the existing protein structure."
  ABORT = "abort"
