namespace PostInstallationRunner.Util;

public class ConstantPaths
{
    /// <summary>
    /// Path of the global temp directory.
    /// </summary>
    public static readonly string TEMP_DIR = @"C:\ProgramData\IBCI\temp";
    /// <summary>
    /// Filepath of the WSL2 distro.
    /// </summary>
    public static readonly string WSL2_DISTRO_TEMP_FILEPATH = $@"{TEMP_DIR}\alma9-ligpargen-rootfs.tar";
    /// <summary>
    /// Program folder of LigParGenGUI.
    /// </summary>
    public static readonly string LIGPARGEN_GUI_PROGRAM_DIR = @"C:\ProgramData\IBCI\LigParGenGUI";
    /// <summary>
    /// Program folder of LigParGenGUI.
    /// </summary>
    public static readonly string LIGPARGEN_GUI_PROGRAM_BIN_DIR = $@"{LIGPARGEN_GUI_PROGRAM_DIR}\bin";
    /// <summary>
    /// Wsl2 folder of IBCI.
    /// </summary>
    public static readonly string WSL_DIR = @"C:\ProgramData\IBCI\wsl";
    /// <summary>
    /// Wsl2 folder of LigParGen.
    /// </summary>
    public static readonly string WSL_LIGPARGEN_GUI_DIR = @"C:\ProgramData\IBCI\wsl\LigParGenGUI";
    /// <summary>
    /// Wsl2 distro storage folder of LigParGenGUI.
    /// </summary>
    public static readonly string WSL_STORAGE_DIR = $@"C:\ProgramData\IBCI\wsl\LigParGen\storage";
    /// <summary>
    /// Filepath of Wsl2 distro vhdx.
    /// </summary>
    public static readonly string WSL_VHDX_FILEPATH = $@"{WSL_STORAGE_DIR}\ext4.vhdx";

    #region Offline win package

    /// <summary>
    /// Filepath of the offline win package zip archive.
    /// </summary>
    public static readonly string INSTALLER_OFFLINE_WIN_PACKAGE_ZIP_FILEPATH = $"{PYSSA_INSTALLER_PROGRAM_DIR}\\offline_win_package.zip";
    /// <summary>
    /// Path of for the extra tools of LigParGenGUI.
    /// </summary>
    public static readonly string PYSSA_EXTRA_TOOLS_PATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\extra_tools";
    /// <summary>
    /// Filepath of the help browser executable.
    /// </summary>
    public static readonly string PYSSA_BROWSER_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\extra_tools\\browser.exe";
    /// <summary>
    /// Path of the win start folder.
    /// </summary>
    public static readonly string PYSSA_WIN_START_PATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start";
    /// <summary>
    /// Path of the images folder for LigParGenGUI.
    /// </summary>
    public static readonly string PYSSA_WIN_START_IMAGES_PATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start\\images";
    /// <summary>
    /// Filepath of the LigParGenGUI windows icon.
    /// </summary>
    public static readonly string PYSSA_WIN_START_IMAGES_ICON_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start\\images\\icon.ico";
    /// <summary>
    /// Path of the start scripts.
    /// </summary>
    public static readonly string PYSSA_WIN_START_VB_SCRIPT_PATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start\\vb_script";
    /// <summary>
    /// Filepath of the PyMOL configuration file (pymolrc).
    /// </summary>
    public static readonly string PYSSA_WIN_START_VB_SCRIPT_PYMOLRC_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start\\vb_script\\.pymolrc.py";
    /// <summary>
    /// Filepath of the batch file to start LigParGenGUI.
    /// </summary>
    public static readonly string PYSSA_WIN_START_VB_SCRIPT_START_BAT_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start\\vb_script\\LigParGenGUI.bat";
    /// <summary>
    /// Filepath of the start vbs script.
    /// </summary>
    public static readonly string PYSSA_WIN_START_VB_SCRIPT_START_VBS_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start\\vb_script\\start.vbs";
    /// <summary>
    /// Filepath of the windows arrangement winbatch script executable.
    /// </summary>
    public static readonly string PYSSA_WIN_START_VB_SCRIPT_WINBATCH_EXE_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\win_start\\vb_script\\window_arrangement.exe";
    /// <summary>
    /// Filepath of the LigParGenGUI license.
    /// </summary>
    public static readonly string PYSSA_LICENSE_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\License.rtf";
    /// <summary>
    /// Filepath of the PyMOL v3 python wheel file.
    /// </summary>
    public static readonly string PYSSA_PYMOL_WHEEL_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\pymol-3.0.0-cp39-cp39-win_amd64.whl";
    /// <summary>
    /// Filepath of a PyMOL configuration file (as pymol script).
    /// </summary>
    public static readonly string PYSSA_PYMOLRC_PML_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\pymolrc.pml";
    /// <summary>
    /// Filepath of the plugin zip file.
    /// </summary>
    public static readonly string PYSSA_PYSSA_ZIP_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\pyssa.zip";
    /// <summary>
    /// Filepath of the LigParGenGUI version (old).  // TODO: Could be removed?!
    /// </summary>
    public static readonly string PYSSA_PYSSA_VERSION_TXT_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\pyssa_version_current.txt";
    /// <summary>
    /// Filepath of the frozen conda environment.
    /// </summary>
    public static readonly string PYSSA_PYSSA_CONDA_ENV_TAR_GZ_FILEPATH = $"{LIGPARGEN_GUI_PROGRAM_DIR}\\pyssa_wo_pymol.tar.gz";
    
    /// <summary>
    /// Path of the mamba root folder for the base env and LigParGenGUI env.
    /// </summary>
    public static readonly string MAMBA_ENV_PATH = @"C:\ProgramData\pyssa\mambaforge_pyssa";
    /// <summary>
    /// Filepath of the conda batch file.
    /// </summary>
    public static readonly string MAMBA_CONDA_BAT_FILEPATH = @"C:\ProgramData\pyssa\mambaforge_pyssa\base-mamba\condabin\conda.bat";
    /// <summary>
    /// Filepath of the conda activate command batch file.
    /// </summary>
    public static readonly string MAMBA_CONDA_ACTIVATE_BAT_FILEPATH = @"C:\ProgramData\pyssa\mambaforge_pyssa\base-mamba\condabin\activate.bat";
    /// <summary>
    /// Filepath of a python module.
    /// </summary>
    public static readonly string MAMBA_BASE_ENV_ABC_PY_FILE_FILEPATH = @"C:\ProgramData\pyssa\mambaforge_pyssa\base-mamba\Lib\_py_abc.py";
    
    /// <summary>
    /// Program path of the LigParGenGUI-Installer.
    /// </summary>
    public static readonly string PYSSA_INSTALLER_PROGRAM_DIR = "C:\\ProgramData\\pyssa-installer";
    

    #endregion
}
