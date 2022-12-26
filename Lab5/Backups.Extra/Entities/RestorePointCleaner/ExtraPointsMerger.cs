using Backups.Entities.Algorithms;
using Backups.Entities.Archivers;
using Backups.Entities.Backup;
using Backups.Entities.Repositories;
using Backups.Extra.Entities.Logger;
using Backups.Models;

namespace Backups.Extra.Entities.RestorePointCleaner;

public class ExtraPointsMerger : IExtraPointsCleaner
{
    private ILogger _logger;

    public ExtraPointsMerger(ILogger logger)
    {
        _logger = logger;
    }

    public void Clean(List<RestorePoint> source, IReadOnlyCollection<RestorePoint> trash, IRepository repository, IAlgorithm algorithm, IArchiver archiver)
    {
        _logger.LogLine($"Merger: start working");
        if (trash.Count == 0)
        {
            _logger.LogLine("Nothing to merge");
            return;
        }

        var saved = source.Except(trash).ToList();
        saved.Sort((a, b) => DateTime.Compare(a.DateTime, b.DateTime));

        RestorePoint oldest = saved.First();

        _logger.LogLine($"Backup timed {oldest.DateTime} chosen as base");

        var contents = new List<IArchiveContent>();
        IArchiveContent oldestContent = oldest.Storage.Content;
        contents.Add(oldestContent);

        var repositoryObjects = oldestContent.Items.ToList();

        var trashList = trash.ToList();
        trashList.Sort((a, b) => DateTime.Compare(b.DateTime, a.DateTime));
        foreach (RestorePoint restorePoint in trashList)
        {
            IArchiveContent currentContent = restorePoint.Storage.Content;
            contents.Add(currentContent);
            foreach (IRepositoryObject repositoryObject in currentContent.Items)
            {
                if (!repositoryObjects.Select(item => item.Name).Contains(repositoryObject.Name))
                {
                    repositoryObjects.Add(repositoryObject);
                    _logger.LogLine($"\'{repositoryObject.Name}\' is added from restore point timed {restorePoint.DateTime}");
                }
            }
        }

        string folderName = "RestorePoint" + oldest.DateTime.ToString("_yyyy_MM_dd_hh_mm_ss") + "_merged";
        _logger.LogLine($"Merged restore point folder name is \'{folderName}\'");

        repository.CreateFolder(new FileSystemPath(folderName));
        IStorage storage = algorithm.Run(repository, new FileSystemPath(folderName), archiver, repositoryObjects);
        var result = new RestorePoint(storage, new FileSystemPath(string.Empty), new FileSystemPath(folderName), oldest.DateTime);
        contents.ForEach(current => current.Dispose());
        foreach (RestorePoint restorePoint in trash)
        {
            repository.RemoveObject(restorePoint.FolderPath);
            _logger.LogLine($"Restore point timed {restorePoint.DateTime} deleted");
        }

        _logger.LogLine($"Deleted: {source.RemoveAll(trash.Contains)}");

        repository.RemoveObject(oldest.FolderPath);
        source.Remove(oldest);
        _logger.LogLine("Base restore point updated");

        source.Add(result);
        _logger.LogLine("Merge completed!");
    }
}