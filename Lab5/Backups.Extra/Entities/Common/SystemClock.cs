namespace Backups.Extra.Entities.Common;

public class SystemClock : IClock
{
    public DateTime DateTime => DateTime.Now;
}