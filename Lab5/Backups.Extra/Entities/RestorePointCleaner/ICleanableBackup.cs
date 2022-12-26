using Backups.Entities.Backup;
using Backups.Entities.Repositories;

namespace Backups.Extra.Entities.RestorePointCleaner;

public interface ICleanableBackup : IBackup
{
    IExtraPointsChooser Chooser { get; }
    IExtraPointsCleaner Cleaner { get; }
    IRepository? Repository { get; set; }
    void Clean();
}