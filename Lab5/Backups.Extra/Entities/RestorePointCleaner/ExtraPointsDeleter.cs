using Backups.Entities.Algorithms;
using Backups.Entities.Archivers;
using Backups.Entities.Backup;
using Backups.Entities.Repositories;
using Backups.Extra.Entities.Logger;

namespace Backups.Extra.Entities.RestorePointCleaner;

public class ExtraPointsDeleter : IExtraPointsCleaner
{
    private ILogger _logger;

    public ExtraPointsDeleter(ILogger logger)
    {
        _logger = logger;
    }

    public void Clean(List<RestorePoint> source, IReadOnlyCollection<RestorePoint> trash, IRepository repository, IAlgorithm algorithm, IArchiver archiver)
    {
        _logger.LogLine("Restore point deleter: start working");
        foreach (RestorePoint restorePoint in trash)
        {
            repository.RemoveObject(restorePoint.FolderPath);
            _logger.LogLine($"Restore point timed \'{restorePoint.DateTime}\' deleted");
        }

        source.RemoveAll(trash.Contains);
        _logger.LogLine("Restore point deleter: finish working");
    }
}