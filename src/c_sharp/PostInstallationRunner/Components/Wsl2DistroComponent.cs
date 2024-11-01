using System.Diagnostics;
using PostInstallationRunner.Util;

namespace PostInstallationRunner.Components;

public class Wsl2DistroComponent : IComponent
{
    /// <summary>
    /// Installs WSL2 distro.
    /// </summary>
    /// <returns>
    /// True if WSL2 distro is successfully installed, otherwise false.
    /// </returns>
    public bool Install()
    {
        #region Checks

        if (!File.Exists(ConstantPaths.WSL2_DISTRO_TEMP_FILEPATH))
        {
            return false;
        }

        #endregion

        if (!Directory.Exists(ConstantPaths.WSL_DIR))
        {
            Directory.CreateDirectory(ConstantPaths.WSL_DIR);
        }
        if (!Directory.Exists(ConstantPaths.WSL_STORAGE_DIR))
        {
            Directory.CreateDirectory(ConstantPaths.WSL_STORAGE_DIR);
        }
        Process process = new Process
        {
            StartInfo =
            {
                FileName = "cmd.exe",
                UseShellExecute = false,
                CreateNoWindow = true,
                Arguments = $"/C wsl --import almaLigParGen9 {ConstantPaths.WSL_STORAGE_DIR} {ConstantPaths.WSL2_DISTRO_TEMP_FILEPATH}"
            }
        };
        try
        {
            process.Start();
            process.WaitForExit();
        }
        catch (Exception ex)
        {
            return false;
        }
        return true;
    }

    /// <summary>
    /// Uninstalls WSL2 distro.
    /// </summary>
    /// <returns>
    /// True if WSL2 distro is successfully uninstalled, otherwise false.
    /// </returns>
    public bool Uninstall()
    {
        Process process = new Process
        {
            StartInfo =
            {
                FileName = "cmd.exe",
                UseShellExecute = false,
                CreateNoWindow = true,
                Arguments = "/C wsl --unregister almaLigParGen9"
            }
        };
        try
        {
            process.Start();
            process.WaitForExit();
        }
        catch (Exception ex)
        {
            return false;
        }

        if (!File.Exists(ConstantPaths.WSL_VHDX_FILEPATH))
        {
            if (Directory.Exists(ConstantPaths.WSL_LIGPARGEN_GUI_DIR))
            {
                Directory.Delete(ConstantPaths.WSL_LIGPARGEN_GUI_DIR, true);
            }
        }
        else
        {
            // Unregistering the WSL2 distro failed therefore return false
            return false;
        }
        return true;
    }

    /// <summary>
    /// Checks if WSL2 distro is installed or not on the system.
    /// </summary>
    /// <returns>
    /// True if WSL2 distro is installed, otherwise false.
    /// </returns>
    public bool IsInstalled()
    {
        Process process = new Process
        {
            StartInfo =
            {
                FileName = "cmd.exe",
                UseShellExecute = false,
                CreateNoWindow = true,
                Arguments = "/C wsl -d almaLigParGen9 ls /home/alma_ligpargen/ligpargen_gui/wsl2"
            }
        };
        try
        {
            process.Start();
            process.WaitForExit();
        }
        catch (Exception ex)
        {
            return false;
        }
        if (process.ExitCode != 0)
        {
            return false;
        }
        return true;
    }
}