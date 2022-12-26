namespace Backups.Extra.Exceptions;

public class RestorePointsLimitsException : BackupsExtraException
{
    protected RestorePointsLimitsException(string? message)
        : base(message) { }

    public static RestorePointsLimitsException NonPositiveAmount()
    {
        return new RestorePointsLimitsException("Amount of stored points must be more than 0");
    }

    public static RestorePointsLimitsException NonPositiveTimeSpan()
    {
        return new RestorePointsLimitsException("Restore points can't be deleted instantly");
    }
}