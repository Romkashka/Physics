using Backups.Entities.Backup;
using Backups.Extra.Models;

namespace Backups.Extra.Entities.RestorePointCleaner.RestorePointChooser;

public interface ISingleChooser
{
    public IReadOnlyList<RestorePoint> Choose(IReadOnlyCollection<RestorePoint> allPointsCollection, RestorePointsLimits restorePointsLimits);
}