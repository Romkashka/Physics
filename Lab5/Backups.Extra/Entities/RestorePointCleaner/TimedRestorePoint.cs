using Backups.Entities.Algorithms;
using Backups.Entities.Backup;
using Backups.Models;

namespace Backups.Extra.Entities.RestorePointCleaner;

public class TimedRestorePoint : IRestorePoint
{
    private IRestorePoint _base;

    public TimedRestorePoint(IRestorePoint @base, DateTime dateTime)
    {
        _base = @base;
        DateTime = dateTime;
    }

    public IStorage Storage => _base.Storage;
    public IPath Path => _base.Path;
    public IPath FolderPath => _base.FolderPath;
    public DateTime DateTime { get; }
}