using Backups.Entities.Backup;
using Backups.Extra.Models;

namespace Backups.Extra.Entities.RestorePointCleaner.RestorePointChooser;

public interface IChooser
{
    public RestorePointsLimits RestorePointsLimits { get; }
    public IEnumerable<RestorePoint> Choose(IReadOnlyCollection<RestorePoint> allPointsCollection);
}