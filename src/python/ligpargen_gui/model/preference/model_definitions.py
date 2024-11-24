import datetime
import enum
import os
import pathlib

from ligpargen_gui.model.util import global_vars


class ModelDefinitions:
  """Global basic definitions for the model.

  Should be used as singleton class!
  """
  if global_vars.DEBUG:
    # <editor-fold desc="For development purposes">
    PROGRAM_ROOT_PATH = pathlib.Path(__file__).parent.parent.parent.parent.parent.parent
    """Path to the root of the program."""
    PROGRAM_SRC_PATH = r"C:\Users\student\github_repos\LigParGen-GUI\src"
    # </editor-fold>
  else:
    # <editor-fold desc="Deployment paths">
    PROGRAM_ROOT_PATH = "C:\\ProgramData\\IBCI\\LigParGenGUI\\bin\\_internal"
    """Path to the root of the program."""
    PROGRAM_SRC_PATH = "C:\\ProgramData\\IBCI\\LigParGenGUI\\bin\\_internal\\src"
    # </editor-fold>
  DISTRO_NAME = "almaLigParGen9"
  """Name of the WSL2 distro"""
  SETTINGS_FILENAME = 'settings.json'
  """Default settings filename"""
  DEFAULT_SETTINGS_PATH: pathlib.Path = pathlib.Path(
    f"{os.path.expanduser('~')}/.ligpargen_gui/"
  )
  DEFAULT_SETTINGS_FILEPATH: pathlib.Path = pathlib.Path(
    f"{os.path.expanduser('~')}/.ligpargen_gui/{SETTINGS_FILENAME}"
  )
  """Default settings path"""
  DEFAULT_LOG_PATH: pathlib.Path = pathlib.Path(f'{DEFAULT_SETTINGS_PATH}/logs')
  """Default logging path"""
  DEFAULT_WINDOWS_LOG_PATH: pathlib.Path = pathlib.Path(f'{DEFAULT_LOG_PATH}/windows')
  """Default Windows logging path"""
  DEFAULT_WSL2_LOG_PATH: pathlib.Path = pathlib.Path(f'{DEFAULT_LOG_PATH}/wsl2')
  """Default WSL2 logging path"""
  LOG_FILENAME = f'{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d}_{datetime.datetime.now().hour:02d}-{datetime.datetime.now().minute:02d}.log'  # noqa: E501
  """Log filename"""
  LOG_FILEPATH = pathlib.Path(f'{DEFAULT_WINDOWS_LOG_PATH}/{LOG_FILENAME}')
  """Complete log filepath"""
  ASSETS_PATH = pathlib.Path(f"{PROGRAM_ROOT_PATH}/assets")
  """Path to the assets folder"""
  ICONS_PATH = pathlib.Path(f"{ASSETS_PATH}/icons")
  """Path to the icons folder"""
  LOGO_FILEPATH = pathlib.Path(f"{ASSETS_PATH}/logo.png")
  """Path to the logo image"""
  STATUS_MESSAGE_TIMEOUT = 5000  # value in msec
  """The standard status bar message timeout"""
  VERSION_NUMBER = "0.1.6"  # The version number MUST be in double quotes
  """The version number of the application"""
  URL_TO_REMOTE_VERSION = "https://w-hs.sciebo.de/s/vTFDNkX8aA6p1cJ/download"
  """The url to the remote version file of the application"""
  REMOTE_VERSION_FILEPATH = pathlib.Path(f"{DEFAULT_SETTINGS_PATH}/remote_version.json")
  """The filepath of the remote version file after its downloaded"""
  URL_TO_UPDATE_SETUP = "https://w-hs.sciebo.de/s/0ZA3494SQbICAbu/download"
  """The url to the update setup file of the application"""


class LigParGenOptions:
  """Class that contains all ligpargen options of the webserver."""
  MOLECULE_OPTIMIZATION_ITERATIONS = ["0", "1", "2", "3"]
  """Options for different molecule optimization iterations supported by the web server."""
  CHARGE_MODEL = ["CM1A-LBCC", "CM1A"]
  """Options for different charge models supported by the web server."""
  MOLECULE_CHARGE = ["0", "-1", "-2", "+1", "+2"]
  """Options for different molecule charges supported by the web server."""


class LigParGenResultFileTypes(enum.StrEnum):
  """Class that contains all result file types of the webserver."""
  APBS_PQR = "apbs.pqr"
  CHARMM_PDB = "charmm.pdb"
  CHARMM_PRM = "charmm.prm"
  CHARMM_RTF = "charmm.rtf"
  DESMOND_CMS = "desmond.cms"
  GROMACS_GRO = "gmx.gro"
  GROMACS_ITP = "gmx.itp"
  LAMMPS_LMP = "lammps.lmp"
  OPENMM_PDB = "openmm.pdb"
  OPENMM_XML = "openmm.xml"
  Q_LIB = "q.lib"
  Q_PDB = "q.pdb"
  Q_PRM = "q.prm"
  TINKER_KEY = "tinker.key"
  TINKER_XYZ = "tinker.xyz"
  XPLOR_PARAM = "xplor.param"
  XPLOR_TOP = "xplor.top"


class JopTypes(enum.StrEnum):
  """Enumeration for storing possible job types."""
  RUN_LIGPARGEN = "RUN LigParGen"
  """Job type for a LigParGen job."""
  INSTALL_BOSS = "INSTALL Boss"
  """Job type for a install BOSS job."""


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
  DROP_DOWN_ARROW = "KEYBOARD_ARROW_DOWN_GREY"
