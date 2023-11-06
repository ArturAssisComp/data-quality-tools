import logging
from typing import Any
import matplotlib.pyplot as plt
from globals.types import SnapshotType

from logger.utils import get_custom_logger_name
from tools.base_result_generator.base_generator import BaseOverviewGenerator
from tools.data_consistency_inspector.snapshot.column_inconsistency_count_by_type.model.model import ColumnInconsistencyCountByTypeSnapshotContent
from utils.file_operations import FileOperations
from utils.plot_operations import PlotOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

# constants
BAR_PLOT_SETTINGS = {
    'relative': {
        'y_label': 'Percentage of Inconsistencies',
        'fig_name': 'rel_ranked_inconsistency_count_by_column_overview.png',
        'suffix': '%'
    },
    'absolute': {
        'y_label': 'Row Count',
        'fig_name': 'abs_ranked_inconsistency_count_by_column_overview.png',
        'suffix': ''
    }
}
CONTENT_SIZE_LIMIT_FOR_TOP_LABEL = 20
CONTENT_SIZE_LIMIT_FOR_X_LABEL = 50
VALUE_SIZE_LIMIT = 1000
X_LABEL = 'Inconsistency Per Column'
TITLE = 'Ranked Inconsistency Count by Column Overview'


class RankedInconsistencyCountByColumnOverviewGenerator(BaseOverviewGenerator):
    _plot_operations:PlotOperations
    _needed_snapshots:list[SnapshotType] = [SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT]
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations=PlotOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
        self._plot_operations = plot_operations
    
    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        column_inconsistency_count_by_type_snapshot_content = parsed_content_dict[SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT]
        column_inconsistency_count_snapshot_content = self._count_by_type_to_count_by_column(column_inconsistency_count_by_type_snapshot_content)

        try:
            try:
                self._generate_bar_plot(column_inconsistency_count_snapshot_content, basedir_path, name_preffix=name_preffix)
            finally:
                plt.close()
            try:
                self._generate_bar_plot(column_inconsistency_count_snapshot_content, basedir_path, relative=True, name_preffix=name_preffix)
            finally:
                plt.close()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')

    def _count_by_type_to_count_by_column(self, column_inconsistency_count_by_type_snapshot_content:ColumnInconsistencyCountByTypeSnapshotContent):
        result:dict[str, int] = dict()
        for key, value in column_inconsistency_count_by_type_snapshot_content.content.items():
            result[key] = sum(value.values())
        return result

    def _should_add_label_on_top(self, content:dict, relative:bool):
        basic_check = len(content) <= CONTENT_SIZE_LIMIT_FOR_TOP_LABEL 
        if relative:
            return basic_check
        return basic_check and max(content.values()) < VALUE_SIZE_LIMIT

    # TODO refactor: extract this function, because it is implemented also in null value inspector tool
    def _generate_bar_plot(self,column_inconsistency_count_snapshot_content:dict[str, int], basedir_path:str, name_preffix:str='', relative:bool=False):
        content = column_inconsistency_count_snapshot_content
        keys:list[str] = []
        values:list[int] = []
        for key, value in sorted(content.items(), key=lambda x:x[1], reverse=True):
            keys.append(key)
            values.append(value)

        total_nulls = sum(values)
        total_columns = len(keys)
        average_value = 100 / total_columns if relative else total_nulls / total_columns

        x = list(keys)
        y = [value/total_nulls * 100 for value in values] if relative else values
        
        if len(y) > CONTENT_SIZE_LIMIT_FOR_X_LABEL:
            x = x[:CONTENT_SIZE_LIMIT_FOR_X_LABEL]
            y = y[:CONTENT_SIZE_LIMIT_FOR_X_LABEL]
                

        
        settings_key = 'relative' if relative else 'absolute'
        settings = BAR_PLOT_SETTINGS[settings_key]
        
        has_label_on_top = self._should_add_label_on_top(content, relative)

        self._plot_operations.plot_figure(list(range(len(x))), y, settings['y_label'], X_LABEL, TITLE, average_value, has_label_on_top, name_preffix + settings['fig_name'], relative, settings['suffix'], basedir_path, x_labels=x)

        self._logger.info(f'{settings["fig_name"]} generated!')





