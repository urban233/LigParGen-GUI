using PostInstallationRunner.Components;

namespace PostInstallationRunner;

class Program
{
    static void Main(string[] args)
    {
        Wsl2DistroComponent tmpWsl2DistroComponent = new Wsl2DistroComponent();
        if (!tmpWsl2DistroComponent.IsInstalled())
        {
            Console.WriteLine("Start installation of WSL2 distro ...");
            if (!tmpWsl2DistroComponent.Install())
            {
                Console.WriteLine("Installation of WSL2 distro failed!");
                Environment.ExitCode = 10; // ERROR_BAD_ENVIRONMENT: https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
                Environment.Exit(Environment.ExitCode);
            }
            Console.WriteLine("Installation of WSL2 distro finished successfully.");
        }
    }
}
