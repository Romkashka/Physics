namespace Backups.Extra.Exceptions;

public class RestorerException : BackupsExtraException
{
    protected RestorerException(string? message)
        : base(message) { }

    public static RestorerException UnknownRepositoryObjectType()
    {
        return new RestorerException("Can't restore repository objects of this type");
    }
}