using Backups.Entities.Backup;
using Backups.Entities.Repositories;

namespace Backups.Extra.Entities.Common;

public interface IRestorer
{
    void Restore(IRepository repository, IRestorePoint restorePoint, bool force);
}