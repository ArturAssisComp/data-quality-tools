import logging
from typing import Any
import matplotlib.pyplot as plt
from globals.types import SnapshotType

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotContent
from tools.base_result_generator.base_generator import BaseOverviewGenerator
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

class NullDistributionByRowOverviewGenerator(BaseOverviewGenerator):
    _needed_snapshots:list[SnapshotType] = [SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT]
    _plot_operations:PlotOperations
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations=PlotOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
        self._plot_operations = plot_operations

    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        rowNullDistributionSnapshotContentModel = parsed_content_dict[SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT]
        try:
            try:
                self._generate_bar_plot(rowNullDistributionSnapshotContentModel, basedir_path, name_preffix=name_preffix)
            finally:
                plt.close()
            try:
                self._generate_bar_plot(rowNullDistributionSnapshotContentModel, basedir_path, relative=True, name_preffix=name_preffix)
            finally:
                plt.close()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')



    def _should_add_label_on_top(self, content, relative):
        basic_check = len(content) <= CONTENT_SIZE_LIMIT and max(content) - min(content) <= MAX_WIDTH
        if relative:
            return basic_check
        return basic_check and max(content.values()) < VALUE_SIZE_LIMIT

    def _generate_bar_plot(self, row_null_distribution_snapshot_content_model:RowNullDistributionSnapshotContent, basedir_path:str, name_preffix:str = '', relative:bool=False):
        content = row_null_distribution_snapshot_content_model.content
        content = dict(sorted(content.items()))

        total_nulls = sum(k * v for k, v in content.items())
        total_rows = sum(content.values())
        average_value = total_nulls / total_rows

        x = list(content.keys())
        y = [value/total_rows * 100 for value in content.values()] if relative else list(content.values())
        
        settings_key = 'relative' if relative else 'absolute'
        settings = BAR_PLOT_SETTINGS[settings_key]
        
        has_label_on_top = self._should_add_label_on_top(content, relative)


        fig_name = name_preffix + settings['fig_name']
        self._plot_operations.plot_figure(x, y, settings['y_label'], X_LABEL, TITLE, average_value, has_label_on_top, fig_name, relative, settings['suffix'], basedir_path)

        self._logger.info(f'{fig_name} generated!')




