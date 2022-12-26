using Backups.Entities.Algorithms;
using Backups.Entities.Archivers;
using Backups.Entities.Backup;
using Backups.Entities.Repositories;
using Backups.Extra.Entities.Logger;
using Backups.Extra.Entities.RestorePointCleaner;
using Backups.Extra.Models;
using Backups.Models;

namespace Backups.Extra.Entities.Common;

public class BackupExtraService : IBackupExtraService
{
    public BackupExtraService(IRepository source, IRepository destination, IAlgorithm algorithm, IArchiver archiver, ILogger logger, IExtraPointsChooser chooser, IExtraPointsCleaner cleaner, IRestorer restorer)
    {
        Source = source;
        Destination = destination;
        Backup = new CleanableBackup(chooser, cleaner);
        BackupTask = new BackupTaskExtended(new BackupTask(destination, algorithm, archiver, Backup), logger);
        Logger = logger;
        Restorer = restorer;
    }

    public IRepository Source { get; }
    public IRepository Destination { get; }
    public ICleanableBackup Backup { get; }
    public IBackupTaskExtended BackupTask { get; }
    public IRestorer Restorer { get; }
    public ILogger Logger { get; }

    public void StartTracking(IPath obj)
    {
        BackupTask.AddBackupObject(new BackupObject(Source, obj));
    }

    public void StopTracking(IPath obj)
    {
        BackupTask.RemoveBackupObject(new BackupObject(Source, obj));
    }

    public IRestorePoint CreateBackup()
    {
        return BackupTask.Run();
    }

    public IRestorePoint CreateBackupWithTime(DateTime dateTime)
    {
        return BackupTask.RunWithTime(dateTime);
    }

    public void RestoreToSource(IRestorePoint restorePoint, bool force)
    {
        Restorer.Restore(Destination, restorePoint, force);
    }

    public void RestoreToCustom(IRepository repository, IRestorePoint restorePoint, bool force)
    {
        Restorer.Restore(repository, restorePoint, force);
    }
}