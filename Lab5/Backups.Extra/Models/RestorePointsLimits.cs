using System.Text;
using Backups.Extra.Exceptions;

namespace Backups.Extra.Models;

public class RestorePointsLimits
{
    public RestorePointsLimits(int maxAmount = int.MaxValue, TimeSpan? maxLifeTime = null)
    {
        MaxAmount = ValidateAmount(maxAmount);
        MaxLifeTime = ValidateTimeSpan(maxLifeTime);
    }

    public int MaxAmount { get; }
    public TimeSpan MaxLifeTime { get; }

    public override string ToString()
    {
        var builder = new StringBuilder();
        builder.AppendLine($"Maximum amount: {MaxAmount}")
            .AppendLine($"Maximum life time: {MaxLifeTime}");
        return builder.ToString();
    }

    private int ValidateAmount(int amount)
    {
        if (amount <= 0)
        {
            throw RestorePointsLimitsException.NonPositiveAmount();
        }

        return amount;
    }

    private TimeSpan ValidateTimeSpan(TimeSpan? timeSpan)
    {
        TimeSpan result = timeSpan ?? TimeSpan.MaxValue / 2;

        if (result.Ticks <= 0)
        {
            throw RestorePointsLimitsException.NonPositiveTimeSpan();
        }

        return result;
    }
}