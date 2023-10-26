import logging
from typing import Any
import matplotlib.pyplot as plt
import pandas as pd
from globals.types import SnapshotType

from tools.null_value_inspector.result_generator.base_generator import BaseOverviewGenerator
from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.column_pair_null_pattern.model.model import ColumnPairNullPatternSnapshotContent
from utils.file_operations import FileOperations
from utils.plot_operations import PlotOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

# constants
FIG_NAME = 'null_frequent_pairs_overview.png'
TOP_10_FIG_NAME = 'top_10_null_frequent_pairs_overview.png'
TITLE = 'Null Frequent Pairs Overview'
TOP_10_TITLE = 'Null Frequent Pairs Overview (top 10)'
MAX_COLUMNS = 40


class NullFrequentPairsOverviewGenerator(BaseOverviewGenerator):
    _needed_snapshots:list[SnapshotType] = [SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT]
    _plot_operations:PlotOperations
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations=PlotOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
        self._plot_operations = plot_operations
    

    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        column_pair_null_pattern_snapshot_content = parsed_content_dict[SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT]
        try:
            self._generate_heatmap(column_pair_null_pattern_snapshot_content, basedir_path, name_preffix=name_preffix)
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')
        finally:
            plt.close()


    def _generate_heatmap(self, column_pair_null_pattern_snapshot_content:ColumnPairNullPatternSnapshotContent, basedir_path:str, name_preffix:str=''):
        content = column_pair_null_pattern_snapshot_content.content
        df = pd.DataFrame(content)
        df[df.isna()] = 0
        df = self._select_top_n_columns(MAX_COLUMNS, df)
        self._plot_operations.plot_heatmap(df, TITLE, basedir_path, name_preffix + FIG_NAME, log_scale=True)
        self._logger.info(f'{FIG_NAME} generated!')
        self._plot_operations.plot_heatmap(df, TITLE, basedir_path, name_preffix + 'rel_' + FIG_NAME, log_scale=True, relative=True)
        self._logger.info(f'{ 'rel_' + FIG_NAME} generated!')

        self._plot_operations.plot_heatmap(self._select_top_n_columns(10, df), TOP_10_TITLE, basedir_path, name_preffix + TOP_10_FIG_NAME)
        self._logger.info(f'{TOP_10_FIG_NAME} generated!')
        self._plot_operations.plot_heatmap(self._select_top_n_columns(10, df), TOP_10_TITLE, basedir_path, name_preffix + 'rel_' + TOP_10_FIG_NAME, relative=True)
        self._logger.info(f'{'rel_' + TOP_10_FIG_NAME} generated!')


    def _select_top_n_columns(self, n:int, df:pd.DataFrame):
        col_max = df.max(axis=0)
        top_columns = list(col_max.sort_values(ascending=False).index[:n])

        return df.loc[top_columns, top_columns]



