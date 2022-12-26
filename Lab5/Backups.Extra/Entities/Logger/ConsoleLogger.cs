namespace Backups.Extra.Entities.Logger;

public class ConsoleLogger : ILogger
{
    public void Log(string logText)
    {
        Console.Write(logText);
    }

    public void LogLine(string logText)
    {
        Console.WriteLine(logText);
    }
}