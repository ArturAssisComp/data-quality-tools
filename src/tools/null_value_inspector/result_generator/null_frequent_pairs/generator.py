import logging
import matplotlib.pyplot as plt

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.column_pair_null_pattern.model.model import ColumnPairNullPatternSnapshotModel
from utils.file_operations import FileOperations
from utils.plot_operations import PlotOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

# constants
FIG_NAME = 'null_frequent_pairs.png'
CONTENT_SIZE_LIMIT_FOR_TOP_LABEL = 20
CONTENT_SIZE_LIMIT_FOR_X_LABEL = 50
VALUE_SIZE_LIMIT = 1000
X_LABEL = 'Null Per Column'
TITLE = 'Null Frequent Pairs Overview'

class NullFrequentPairsOverviewGenerator:
    _logger:logging.Logger
    _fileOperations:FileOperations
    _plot_operations:PlotOperations
    _column_pair_null_pattern_snapshot:ColumnPairNullPatternSnapshotModel
    _column_pair_null_pattern_snapshot_filepath:str
    _base_result_filepath:str
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations = PlotOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
        self._plot_operations = plot_operations
    
    def generate_overview(self, column_pair_null_pattern_snapshot_filepath:str, base_result_filepath:str):
        self._logger.info('Creating overview')
        self._column_pair_null_pattern_snapshot = ColumnPairNullPatternSnapshotModel(** self._fileOperations.read_Json(column_pair_null_pattern_snapshot_filepath))
        self._column_pair_null_pattern_snapshot_filepath = column_pair_null_pattern_snapshot_filepath
        self._base_result_filepath = base_result_filepath
        try:
            self._generate_heatmap()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')
        finally:
            plt.close()


    def _generate_heatmap(self):
        content = self._column_pair_null_pattern_snapshot.content


        self._logger.info(f'{FIG_NAME} generated!')

