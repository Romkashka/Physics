using Backups.Entities.Algorithms;
using Backups.Entities.Archivers;
using Backups.Entities.Backup;
using Backups.Entities.Repositories;
using Backups.Extra.Entities.Logger;
using Backups.Extra.Entities.RestorePointCleaner;
using Backups.Models;

namespace Backups.Extra.Entities.Common;

public class BackupTaskExtended : IBackupTaskExtended
{
    private IBackupTask _backupTask;

    public BackupTaskExtended(IBackupTask backupTask, ILogger logger)
    {
        _backupTask = backupTask;
        Logger = logger;
        if (Backup is CleanableBackup cleanableBackup)
        {
            cleanableBackup.Algorithm = Algorithm;
            cleanableBackup.Archiver = Archiver;
            cleanableBackup.Repository = Repository;
        }
    }

    public IRepository Repository => _backupTask.Repository;
    public IAlgorithm Algorithm => _backupTask.Algorithm;
    public IArchiver Archiver => _backupTask.Archiver;
    public IReadOnlyCollection<BackupObject> TrackedObjects => _backupTask.TrackedObjects;
    public IBackup Backup => _backupTask.Backup;
    public ILogger Logger { get; }

    public void AddBackupObject(BackupObject backupObject)
    {
        _backupTask.AddBackupObject(backupObject);
        Logger.LogLine($"Backup task extended: add {backupObject.FullPath}");
    }

    public bool RemoveBackupObject(BackupObject backupObject)
    {
        bool result = _backupTask.RemoveBackupObject(backupObject);
        Logger.LogLine($"Backup task extended: add {backupObject.FullPath}");
        return result;
    }

    public IRestorePoint Run()
    {
        Logger.LogLine("Backup task extended: start job!");
        IRestorePoint result = _backupTask.Run();
        Logger.LogLine("Job ended!!!");
        return result;
    }

    public IRestorePoint RunWithTime(DateTime dateTime)
    {
        string folderName = "RestorePoint" + dateTime.ToString("_yyyy_MM_dd_hh_mm_ss");
        Repository.CreateFolder(new FileSystemPath(folderName));
        var repositoryObjects = new List<IRepositoryObject>();
        foreach (BackupObject trackedObject in TrackedObjects)
        {
            repositoryObjects.Add(trackedObject.RepositoryObject);
        }

        IStorage storage = Algorithm.Run(
            Repository,
            new FileSystemPath(folderName),
            Archiver,
            repositoryObjects);

        var result = new RestorePoint(storage, new FileSystemPath(string.Empty), new FileSystemPath(folderName), dateTime);
        Backup.AddRestorePoint(result);
        return result;
    }
}