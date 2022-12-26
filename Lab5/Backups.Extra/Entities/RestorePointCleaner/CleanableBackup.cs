using Backups.Entities.Algorithms;
using Backups.Entities.Archivers;
using Backups.Entities.Backup;
using Backups.Entities.Repositories;
using Backups.Extra.Entities.Common;
using Backups.Extra.Exceptions;
using Backups.Extra.Models;

namespace Backups.Extra.Entities.RestorePointCleaner;

public class CleanableBackup : IBackup, ICleanableBackup
{
    private List<RestorePoint> _restorePoints;
    public CleanableBackup(IExtraPointsChooser chooser, IExtraPointsCleaner cleaner)
    {
        Chooser = chooser;
        Cleaner = cleaner;
        _restorePoints = new List<RestorePoint>();
    }

    public IReadOnlyCollection<RestorePoint> RestorePoints => _restorePoints;

    public IExtraPointsChooser Chooser { get; }
    public IExtraPointsCleaner Cleaner { get; }
    public IRepository? Repository { get; set; }
    public IAlgorithm? Algorithm { get; set; }
    public IArchiver? Archiver { get; set; }
    public void AddRestorePoint(RestorePoint restorePoint)
    {
        _restorePoints.Add(restorePoint);
        Clean();
    }

    public void Clean()
    {
        if (Repository is null)
        {
            throw CleanableBackupException.RepositoryIsntSet();
        }

        if (Algorithm is null)
        {
            throw CleanableBackupException.AlgorithmIsntSet();
        }

        if (Archiver is null)
        {
            throw CleanableBackupException.ArchiverIsntSet();
        }

        IReadOnlyList<RestorePoint> trash = Chooser.Choose(RestorePoints);
        Cleaner.Clean(_restorePoints, trash, Repository, Algorithm, Archiver);
    }
}