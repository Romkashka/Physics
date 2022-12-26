using Backups.Entities.Backup;
using Backups.Extra.Entities.Logger;
using Backups.Extra.Models;

namespace Backups.Extra.Entities.RestorePointCleaner.RestorePointChooser;

public class ChooserByAmount : ISingleChooser
{
    public IReadOnlyList<RestorePoint> Choose(IReadOnlyCollection<RestorePoint> allPointsCollection, RestorePointsLimits restorePointsLimits)
    {
        var allPoints = allPointsCollection.ToList();
        allPoints.Sort((a, b) => DateTime.Compare(a.DateTime, b.DateTime));
        return allPoints.Take(Math.Max(0, allPoints.Count - restorePointsLimits.MaxAmount)).ToList();
    }
}