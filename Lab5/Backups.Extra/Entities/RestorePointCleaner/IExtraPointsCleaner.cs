using Backups.Entities.Algorithms;
using Backups.Entities.Archivers;
using Backups.Entities.Backup;
using Backups.Entities.Repositories;

namespace Backups.Extra.Entities.RestorePointCleaner;

public interface IExtraPointsCleaner
{
    void Clean(List<RestorePoint> source, IReadOnlyCollection<RestorePoint> trash, IRepository repository, IAlgorithm algorithm, IArchiver archiver);
}