namespace Backups.Extra.Exceptions;

public class BackupsExtraException : Exception
{
    protected BackupsExtraException(string? message)
        : base(message) { }
}