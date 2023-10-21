import logging
import matplotlib.pyplot as plt

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotModel
from utils.file_operations import FileOperations
from utils.plot_operations import PlotOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

# constants
BAR_PLOT_SETTINGS = {
    'relative': {
        'y_label': 'Percentage of Rows',
        'fig_name': 'rel_null_distribution_by_row_overview.png',
        'suffix': '%'
    },
    'absolute': {
        'y_label': 'Row Count',
        'fig_name': 'abs_null_distribution_by_row_overview.png',
        'suffix': ''
    }
}
CONTENT_SIZE_LIMIT = 20
VALUE_SIZE_LIMIT = 1000
MAX_WIDTH = 25
X_LABEL = 'Null Per Row'
TITLE = 'Null Distribution by Row Overview'

class NullDistributionByRowOverviewGenerator:
    _logger:logging.Logger
    _fileOperations:FileOperations
    _plot_operations:PlotOperations
    _row_null_distribution_snapshot:RowNullDistributionSnapshotModel
    _row_null_distribution_snapshot_filepath:str
    _base_result_filepath:str
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations=PlotOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
        self._plot_operations = plot_operations
    
    def generate_overview(self, row_null_distribution_snapshot_filepath:str, base_result_filepath:str):
        self._logger.info('Creating overview')
        self._row_null_distribution_snapshot = RowNullDistributionSnapshotModel(** self._fileOperations.read_Json(row_null_distribution_snapshot_filepath))
        self._row_null_distribution_snapshot_filepath = row_null_distribution_snapshot_filepath
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



    def _should_add_label_on_top(self, content, relative):
        basic_check = len(content) <= CONTENT_SIZE_LIMIT and max(content) - min(content) <= MAX_WIDTH
        if relative:
            return basic_check
        return basic_check and max(content.values()) < VALUE_SIZE_LIMIT

    def _generate_bar_plot(self, relative:bool=False):
        content = self._row_null_distribution_snapshot.content
        content = dict(sorted(content.items()))

        total_nulls = sum(k * v for k, v in content.items())
        total_rows = sum(content.values())
        average_value = total_nulls / total_rows

        x = list(content.keys())
        y = [value/total_rows * 100 for value in content.values()] if relative else list(content.values())
        
        settings_key = 'relative' if relative else 'absolute'
        settings = BAR_PLOT_SETTINGS[settings_key]
        
        has_label_on_top = self._should_add_label_on_top(content, relative)


        self._plot_operations.plot_figure(x, y, settings['y_label'], X_LABEL, TITLE, average_value, has_label_on_top, settings['fig_name'], relative, settings['suffix'], self._base_result_filepath)

        self._logger.info(f'{settings["fig_name"]} generated!')

