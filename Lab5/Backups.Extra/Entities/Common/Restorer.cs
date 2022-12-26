using Backups.Entities.Backup;
using Backups.Entities.Repositories;
using Backups.Extra.Entities.Logger;
using Backups.Extra.Exceptions;
using Backups.Models;

namespace Backups.Extra.Entities.Common;

public class Restorer : IRestorer
{
    private ILogger _logger;

    public Restorer(ILogger logger)
    {
        _logger = logger;
    }

    public void Restore(IRepository repository, IRestorePoint restorePoint, bool force)
    {
        using IArchiveContent content = restorePoint.Storage.Content;
        foreach (IRepositoryObject repositoryObject in content.Items)
        {
            _logger.LogLine($"Restorer: restoring into \'{repository.RootPath}\'");
            RestoreObject(repository, repositoryObject, force);
            _logger.LogLine("Restorer: finish job");
        }
    }

    private void RestoreObject(IRepository repository, IRepositoryObject obj, bool force)
    {
        if (obj is IFileRepositoryObject fileRepositoryObject)
        {
            Stream toStream = repository.CreateFile(new FileSystemPath(fileRepositoryObject.Name), force);
            Stream fromStream = fileRepositoryObject.Stream;
            fromStream.CopyTo(toStream);
            toStream.Dispose();
            fromStream.Dispose();
            _logger.LogLine($"File \'{fileRepositoryObject.Name}\' restored");
        }
        else if (obj is IFolderRepositoryObject folderRepositoryObject)
        {
            foreach (IRepositoryObject repositoryObject in folderRepositoryObject.GetEntries)
            {
                _logger.LogLine($"Start restoring folder \'{folderRepositoryObject.Name}\'");
                RestoreObject(repository, repositoryObject, force);
                _logger.LogLine($"Folder \'{folderRepositoryObject.Name}\' fully restored");
            }
        }
        else
        {
            var exception = RestorerException.UnknownRepositoryObjectType();
            _logger.LogLine($"Restorer: ERROR: {exception.Message}");
            throw exception;
        }
    }
}