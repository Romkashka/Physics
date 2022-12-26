using Backups.Entities.Backup;

namespace Backups.Extra.Entities.RestorePointCleaner;

public interface IExtraPointsChooser
{
    IReadOnlyList<RestorePoint> Choose(IReadOnlyCollection<RestorePoint> allPointsCollection);
}