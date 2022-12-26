using System.Text;
using Backups.Entities.Backup;
using Backups.Extra.Entities.Logger;
using Backups.Extra.Models;

namespace Backups.Extra.Entities.RestorePointCleaner.RestorePointChooser;

public class MultiCriteriaChooser : IExtraPointsChooser
{
    private readonly List<ISingleChooser> _singleChoosers;
    private readonly ILogger _logger;

    public MultiCriteriaChooser(
        RestorePointsLimits restorePointsLimits,
        Func<IEnumerable<bool>, bool> decisionMaker,
        IReadOnlyList<ISingleChooser> singleChoosers,
        ILogger logger)
    {
        RestorePointsLimits = restorePointsLimits;
        DecisionMaker = decisionMaker;
        _logger = logger;
        _singleChoosers = singleChoosers.ToList();
    }

    public RestorePointsLimits RestorePointsLimits { get; }
    public Func<IEnumerable<bool>, bool> DecisionMaker { get; }
    public IReadOnlyList<RestorePoint> Choose(IReadOnlyCollection<RestorePoint> allPointsCollection)
    {
        _logger.LogLine("Restore point chooser: start working");

        if (allPointsCollection.Count == 0)
        {
            _logger.LogLine("There is nothing to choose from");
            return new List<RestorePoint>();
        }

        var toDelete = allPointsCollection.Where(point => DecisionMaker(from algorithm in _singleChoosers
            select algorithm.Choose(allPointsCollection, RestorePointsLimits).Contains(point))).ToList();

        _logger.LogLine($"Chosen {toDelete.Count} out of {allPointsCollection.Count} points");
        if (toDelete.Count.Equals(allPointsCollection.Count))
        {
            toDelete.Remove(toDelete.FindLast(t => true) !);
            _logger.LogLine("All points was chosen, so last removed from the list");
        }

        var builder = new StringBuilder();
        builder.AppendLine("Chosen restore points:");
        toDelete.ForEach(current => builder.AppendLine(current.FolderPath.StringPath));
        _logger.Log(builder.ToString());

        return toDelete;
    }
}