import logging
from typing import Any
import matplotlib.pyplot as plt
from globals.types import SnapshotType

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.result_generator.base_generator import BaseOverviewGenerator
from tools.null_value_inspector.snapshot.column_null_count.model.model import ColumnNullCountSnapshotContent
from utils.file_operations import FileOperations
from utils.plot_operations import PlotOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

# constants
BAR_PLOT_SETTINGS = {
    'relative': {
        'y_label': 'Percentage of Nulls',
        'fig_name': 'rel_ranked_null_count_by_column_overview.png',
        'suffix': '%'
    },
    'absolute': {
        'y_label': 'Row Count',
        'fig_name': 'abs_ranked_null_count_by_column_overview.png',
        'suffix': ''
    }
}
CONTENT_SIZE_LIMIT_FOR_TOP_LABEL = 20
CONTENT_SIZE_LIMIT_FOR_X_LABEL = 50
VALUE_SIZE_LIMIT = 1000
X_LABEL = 'Null Per Column'
TITLE = 'Ranked Null Count by Column Overview'


class RankedNullCountByColumnOverviewGenerator2(BaseOverviewGenerator):
    _plot_operations:PlotOperations
    _needed_snapshots:list[SnapshotType] = [SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT]
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations=PlotOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
        self._plot_operations = plot_operations
    
    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        column_null_count_snapshot_content = parsed_content_dict[SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT]
        try:
            try:
                self._generate_bar_plot(column_null_count_snapshot_content, basedir_path, name_preffix=name_preffix)
            finally:
                plt.close()
            try:
                self._generate_bar_plot(column_null_count_snapshot_content, basedir_path, relative=True, name_preffix=name_preffix)
            finally:
                plt.close()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')


    def _should_add_label_on_top(self, content:dict, relative:bool):
        basic_check = len(content) <= CONTENT_SIZE_LIMIT_FOR_TOP_LABEL 
        if relative:
            return basic_check
        return basic_check and max(content.values()) < VALUE_SIZE_LIMIT

    def _generate_bar_plot(self,column_null_count_snapshot_content_model:ColumnNullCountSnapshotContent, basedir_path:str, name_preffix:str='', relative:bool=False):
        content = column_null_count_snapshot_content_model.content
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





