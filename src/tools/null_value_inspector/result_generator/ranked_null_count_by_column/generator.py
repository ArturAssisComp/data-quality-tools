import logging
import matplotlib.pyplot as plt

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.column_null_count.model.model import ColumnNullCountSnapshotModel
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

class RankedNullCountByColumnOverviewGenerator:
    _logger:logging.Logger
    _fileOperations:FileOperations
    _plot_operations:PlotOperations
    _column_null_count_snapshot:ColumnNullCountSnapshotModel
    _column_null_count_snapshot_filepath:str
    _base_result_filepath:str
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations = PlotOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
        self._plot_operations = plot_operations
    
    def generate_overview(self, column_null_count_snapshot_filepath:str, base_result_filepath:str):
        self._logger.info('Creating overview')
        self._column_null_count_snapshot = ColumnNullCountSnapshotModel(** self._fileOperations.read_Json(column_null_count_snapshot_filepath))
        self._column_null_count_snapshot_filepath = column_null_count_snapshot_filepath
        self._base_result_filepath = base_result_filepath
        try:
            try:
                self._generate_bar_plot()
            finally:
                plt.close()
            try:
                self._generate_bar_plot(relative=True)
            finally:
                plt.close()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')



    def _should_add_label_on_top(self, content:dict, relative:bool):
        basic_check = len(content) <= CONTENT_SIZE_LIMIT_FOR_TOP_LABEL 
        if relative:
            return basic_check
        return basic_check and max(content.values()) < VALUE_SIZE_LIMIT

    def _generate_bar_plot(self, relative:bool=False):
        content = self._column_null_count_snapshot.content
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

        self._plot_operations.plot_figure(list(range(len(x))), y, settings['y_label'], X_LABEL, TITLE, average_value, has_label_on_top, settings['fig_name'], relative, settings['suffix'], self._base_result_filepath, x_labels=x)

        self._logger.info(f'{settings["fig_name"]} generated!')

