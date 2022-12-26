using Backups.Entities.Backup;
using Backups.Entities.Repositories;
using Backups.Extra.Entities.Logger;
using Backups.Extra.Entities.RestorePointCleaner;
using Backups.Models;

namespace Backups.Extra.Entities.Common;

public interface IBackupExtraService
{
    public IRepository Source { get; }
    public IRepository Destination { get; }
    public ICleanableBackup Backup { get; }
    public IBackupTaskExtended BackupTask { get; }
    public IRestorer Restorer { get; }
    public ILogger Logger { get; }
    void StartTracking(IPath obj);
    void StopTracking(IPath obj);

    IRestorePoint CreateBackup();
    IRestorePoint CreateBackupWithTime(DateTime dateTime);

    public void RestoreToSource(IRestorePoint restorePoint, bool force);
    public void RestoreToCustom(IRepository repository, IRestorePoint restorePoint, bool force);
}