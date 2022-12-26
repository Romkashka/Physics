using Backups.Entities.Backup;

namespace Backups.Extra.Entities.Common;

public interface IBackupTaskExtended : IBackupTask
{
    public IRestorePoint RunWithTime(DateTime dateTime);
}