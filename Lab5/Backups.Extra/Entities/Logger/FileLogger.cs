using Backups.Entities.Repositories;
using Backups.Models;

namespace Backups.Extra.Entities.Logger;

public class FileLogger : ILogger, IDisposable
{
    private Stream _logFileStream;
    private StreamWriter _writer;

    public FileLogger(IRepository repository, IPath relevantPath)
    {
        _logFileStream = repository.CreateFile(relevantPath, true);
        _writer = new StreamWriter(_logFileStream);
    }

    public void Log(string logText)
    {
        _writer.Write(logText);
    }

    public void LogLine(string logText)
    {
        _writer.WriteLine(logText);
    }

    public void Dispose()
    {
        _writer.Dispose();
        _logFileStream.Dispose();
    }
}