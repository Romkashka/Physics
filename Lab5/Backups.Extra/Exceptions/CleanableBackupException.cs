namespace Backups.Extra.Exceptions;

public class CleanableBackupException : BackupsExtraException
{
    protected CleanableBackupException(string? message)
        : base(message) { }

    public static CleanableBackupException RepositoryIsntSet()
    {
        return new CleanableBackupException("Restore points can't be cleaned: repository isn't specified");
    }

    public static CleanableBackupException AlgorithmIsntSet()
    {
        return new CleanableBackupException("Restore points can't be cleaned: algorithm isn't specified");
    }

    public static CleanableBackupException ArchiverIsntSet()
    {
        return new CleanableBackupException("Restore points can't be cleaned: archiver isn't specified");
    }
}