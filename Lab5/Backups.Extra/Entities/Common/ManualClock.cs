namespace Backups.Extra.Entities.Common;

public class ManualClock : IClock
{
    public ManualClock(DateTime dateTime)
    {
        DateTime = dateTime;
    }

    public DateTime DateTime { get; private set; }

    public void Forward(TimeSpan timeSpan)
    {
        DateTime += timeSpan;
    }
}