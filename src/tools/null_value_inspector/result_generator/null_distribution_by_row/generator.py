import logging
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotModel
from utils.file_operations import FileOperations

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
    _row_null_distribution_snapshot:RowNullDistributionSnapshotModel
    _row_null_distribution_snapshot_filepath:str
    _base_result_filepath:str
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
    
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

        self._plot_figure(x, y, settings['y_label'], X_LABEL, TITLE, average_value, has_label_on_top, settings['fig_name'], relative, settings['suffix'])

        self._logger.info(f'{settings["fig_name"]} generated!')


    def _plot_figure(self, x:list[int], y:list[float]|list[int], y_label:str, x_label:str, title:str, average_value:float, has_label_on_top:bool, fig_name:str, relative:bool, suffix:str):
        # Use a style for the plot
        plt.style.use('ggplot')

        # Create a color map
        cmap = plt.get_cmap('viridis')

        # Create a bar chart with color map
        bars = plt.bar(x, y, color=cmap(np.linspace(0, 1, len(y))))

        # Label the axes
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # Add a title
        plt.title(title)

        # Add a vertical line at the average value
        plt.axvline(average_value, color='r', linestyle='--', label=f'Average: {average_value:.2f}')
        plt.legend()  # Display the legend to show what the vertical line represents


        # Add data labels on top of the bars
        if has_label_on_top:
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}{suffix}', va='bottom', ha='center') # Add percentage sign to the label

        # Ensure x-axis only displays integer values
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        if relative:
            # Format the y-tick labels to display percentages
            plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter())

        # Save the plot to a PNG file with high resolution
        plt.savefig(os.path.join(self._base_result_filepath, fig_name), dpi=300)
        plt.close()

