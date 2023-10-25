import logging
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
    _plot_operations:PlotOperations
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations=PlotOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
        self._plot_operations = plot_operations
    
    def _generate_specific_overview(self, basedir_path: str):
        column_pair_null_pattern_snapshot = self._snapshots[SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT]

        if column_pair_null_pattern_snapshot  is None:
            self._logger.error(f'Invalid snapshot: {SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT.value}')
            raise RuntimeError('Invalid Snapshot')

        if column_pair_null_pattern_snapshot.population:
            column_pair_null_pattern_snapshot_content_model = ColumnPairNullPatternSnapshotContent(content=column_pair_null_pattern_snapshot.population['content'])
            try:
                self._generate_heatmap(column_pair_null_pattern_snapshot_content_model, basedir_path)
            except Exception as e:
                self._logger.error(f'Result not generated: {e}')
            finally:
                plt.close()
        elif column_pair_null_pattern_snapshot.samples:
            pass
        else:
            self._logger.error('Invalid snapshot format')

    def _generate_heatmap(self, column_pair_null_pattern_snapshot_content:ColumnPairNullPatternSnapshotContent, basedir_path:str, name_preffix:str=''):
        content = column_pair_null_pattern_snapshot_content.content
        df = pd.DataFrame(content)
        df[df.isna()] = 0
        df = self._select_top_n_columns(MAX_COLUMNS, df)
        self._plot_operations.plot_heatmap(df, TITLE, basedir_path, name_preffix + FIG_NAME, log_scale=True)
        self._logger.info(f'{FIG_NAME} generated!')

        self._plot_operations.plot_heatmap(self._select_top_n_columns(10, df), TOP_10_TITLE, basedir_path, name_preffix + TOP_10_FIG_NAME)
        self._logger.info(f'{TOP_10_FIG_NAME} generated!')


    def _select_top_n_columns(self, n:int, df:pd.DataFrame):
        col_max = df.max(axis=0)
        top_columns = list(col_max.sort_values(ascending=False).index[:n])

        return df.loc[top_columns, top_columns]



