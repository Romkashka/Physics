using Backups.Entities.Backup;
using Backups.Extra.Entities.Common;
using Backups.Extra.Models;

namespace Backups.Extra.Entities.RestorePointCleaner.RestorePointChooser;

public class ChooserByDate : ISingleChooser
{
    private IClock _clock;

    public ChooserByDate(IClock clock)
    {
        _clock = clock;
    }

    public IReadOnlyList<RestorePoint> Choose(IReadOnlyCollection<RestorePoint> allPointsCollection, RestorePointsLimits restorePointsLimits)
    {
        var allPoints = allPointsCollection.ToList();
        allPoints.Sort((a, b) => DateTime.Compare(a.DateTime, b.DateTime));
        return allPoints.Where(point => restorePointsLimits.MaxLifeTime < new TimeSpan(_clock.DateTime.Ticks - point.DateTime.Ticks)).ToList();
    }
}