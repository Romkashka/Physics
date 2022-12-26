namespace Backups.Extra.Entities.Logger;

public interface ILogger
{
    public void Log(string logText);

    public void LogLine(string logText);
}