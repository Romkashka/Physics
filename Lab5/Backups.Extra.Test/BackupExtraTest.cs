using Backups.Entities.Algorithms;
using Backups.Entities.Archivers;
using Backups.Extra.Entities.Common;
using Backups.Extra.Entities.Logger;
using Backups.Extra.Entities.RestorePointCleaner;
using Backups.Extra.Entities.RestorePointCleaner.RestorePointChooser;
using Backups.Extra.Models;
using Backups.Models;
using Backups.Test.Repository;
using Xunit;
using Zio.FileSystems;

namespace Backups.Extra.Test;

public class BackupExtraTest : IDisposable
{
    private readonly MemoryFileSystem _fileSystem;
    private readonly InMemoryRepository _source;

    public BackupExtraTest()
    {
        _fileSystem = new MemoryFileSystem();
        _source = new InMemoryRepository(new FileSystemPath("/source"), _fileSystem);
        _source.CreateFile(new FileSystemPath(@"/a.txt")).Dispose();
        _source.CreateFolder(new FileSystemPath(@"/Nested"));
        _source.CreateFile(new FileSystemPath(@"/Nested/b.txt")).Dispose();
    }

    [Fact]
    public void CheckMerge()
    {
        var dest = new InMemoryRepository(new FileSystemPath("/dest"), _fileSystem);
        var logger = new ConsoleLogger();
        var clock = new ManualClock(DateTime.Now);
        var dataChooser = new ChooserByDate(clock);
        var amountChooser = new ChooserByAmount();
        IBackupExtraService service = new BackupExtraService(
            _source,
            dest,
            new SingleAlgorithm(),
            new ZipArchiver(),
            logger,
            new MultiCriteriaChooser(
                new RestorePointsLimits(5, new TimeSpan(7, 0, 0, 0)),
                results => results.Any(t => t),
                new List<ISingleChooser>() { amountChooser, dataChooser },
                logger),
            new ExtraPointsMerger(logger),
            new Restorer(logger));
        service.StartTracking(new FileSystemPath("/a.txt"));
        service.StartTracking(new FileSystemPath(@"/Nested/b.txt"));
        service.CreateBackupWithTime(clock.DateTime);
        clock.Forward(new TimeSpan(1, 0, 0, 0));
        service.StopTracking(new FileSystemPath("/Nested/b.txt"));
        for (int i = 0; i < 5; i++)
        {
            service.CreateBackupWithTime(clock.DateTime);
            clock.Forward(new TimeSpan(1, 0, 0, 0));
        }

        Assert.Equal(5, service.Backup.RestorePoints.Count);

        clock.Forward(new TimeSpan(10, 0, 0, 0));
        service.CreateBackup();
        Assert.Equal(1, service.Backup.RestorePoints.Count);
    }

    public void Dispose()
    {
        _fileSystem.Dispose();
    }
}