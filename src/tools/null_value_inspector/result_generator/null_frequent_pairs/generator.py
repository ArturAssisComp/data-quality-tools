import logging
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.column_pair_null_pattern.model.model import ColumnPairNullPatternSnapshotModel
from utils.file_operations import FileOperations
from utils.plot_operations import PlotOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

# constants
FIG_NAME = 'null_frequent_pairs_overview.png'
TOP_10_FIG_NAME = 'top_10_null_frequent_pairs_overview.png'
TITLE = 'Null Frequent Pairs Overview'
TOP_10_TITLE = 'Null Frequent Pairs Overview (top 10)'
MAX_COLUMNS = 40

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
        df = pd.DataFrame(content)
        df[df.isna()] = 0
        df = self._select_top_n_columns(MAX_COLUMNS, df)
        self._plot_operations.plot_heatmap(df, TITLE, self._base_result_filepath, FIG_NAME, log_scale=True)
        self._logger.info(f'{FIG_NAME} generated!')

        self._plot_operations.plot_heatmap(self._select_top_n_columns(10, df), TOP_10_TITLE, self._base_result_filepath, TOP_10_FIG_NAME)
        self._logger.info(f'{TOP_10_FIG_NAME} generated!')


    def _select_top_n_columns(self, n:int, df:pd.DataFrame):
        col_max = df.max(axis=0)
        top_columns = list(col_max.sort_values(ascending=False).index[:n])

        return df.loc[top_columns, top_columns]

