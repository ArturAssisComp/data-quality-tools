import logging
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotModel
from utils.file_operations import FileOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))

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
                self._generate_bar_plot_by_percentage()
            finally:
                plt.close()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')


    # TODO refactor the generate bar plot absolute and relative
    def _generate_bar_plot(self):
        # parameters
        TITLE = 'Null Distribution by Row Overview'
        X_LABEL = 'Null Per Row'
        Y_LABEL = 'Row Count'
        CONTENT_SIZE_LIMIT = 20
        VALUE_SIZE_LIMIT = 1000
        FIG_NAME = 'abs_null_distribution_by_row_overview.png'
        MAX_WIDTH = 25

        # Use a style for the plot
        plt.style.use('ggplot')

        content = self._row_null_distribution_snapshot.content

        # Sort the dictionary by key
        content = dict(sorted(content.items()))

        # calculate average value
        total_nulls = sum(k * v for k, v in content.items())
        total_rows = sum(content.values())
        average_value = total_nulls / total_rows

        # Create lists of keys and values
        x = list(content.keys())
        y = list(content.values())

        # Create a color map
        cmap = plt.get_cmap('viridis')

        # Create a bar chart with color map
        bars = plt.bar(x, y, color=cmap(np.linspace(0, 1, len(y))))

        # Label the axes
        plt.xlabel(X_LABEL)
        plt.ylabel(Y_LABEL)

        # Add a title
        plt.title(TITLE)

        # Add a vertical line at the average value
        plt.axvline(average_value, color='r', linestyle='--', label=f'Average: {average_value:.2f}')
        plt.legend()  # Display the legend to show what the vertical line represents


        # Add data labels on top of the bars
        if len(content) <= CONTENT_SIZE_LIMIT and max(content.values()) < VALUE_SIZE_LIMIT and  max(content) - min(content) <= MAX_WIDTH:
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval}', va='bottom', ha='center') # va: vertical alignment, ha: horizontal alignment

        # Ensure x-axis only displays integer values
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        # Save the plot to a PNG file with high resolution
        plt.savefig(os.path.join(self._base_result_filepath, FIG_NAME), dpi=300)
        plt.close()
        self._logger.info('abs_null_distribution_by_row_overview.png generated!')

    def _generate_bar_plot_by_percentage(self):
        # parameters
        TITLE = 'Null Distribution by Row Overview'
        X_LABEL = 'Null Per Row'
        Y_LABEL = 'Percentage of Rows'  # Update the y-axis label
        CONTENT_SIZE_LIMIT = 20
        MAX_WIDTH = 25
        FIG_NAME = 'rel_null_distribution_by_row_overview.png'

        # Use a style for the plot
        plt.style.use('ggplot')

        content = self._row_null_distribution_snapshot.content

        # Sort the dictionary by key
        content = dict(sorted(content.items()))

        # calculate average value
        total_nulls = sum(k * v for k, v in content.items())
        total_rows = sum(content.values())
        average_value = total_nulls / total_rows

        # Create lists of keys and values
        x = list(content.keys())
        total_rows = sum(content.values())
        y = [value/total_rows * 100 for value in content.values()]  # Convert y values to percentages

        # Create a color map
        cmap = plt.get_cmap('viridis')

        # Create a bar chart with color map
        bars = plt.bar(x, y, color=cmap(np.linspace(0, 1, len(y))))

        # Label the axes
        plt.xlabel(X_LABEL)
        plt.ylabel(Y_LABEL)

        # Add a title
        plt.title(TITLE)

        # Add a vertical line at the average value
        plt.axvline(average_value, color='r', linestyle='--', label=f'Average: {average_value:.2f}')
        plt.legend()  # Display the legend to show what the vertical line represents

        # Add data labels on top of the bars
        if len(content) <= CONTENT_SIZE_LIMIT and max(content) - min(content) <= MAX_WIDTH:
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}%', va='bottom', ha='center') # Add percentage sign to the label

        # Ensure x-axis only displays integer values
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        # Format the y-tick labels to display percentages
        plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter())

        # Save the plot to a PNG file with high resolution
        plt.savefig(os.path.join(self._base_result_filepath, FIG_NAME), dpi=300)
        plt.close()
        self._logger.info('rel_null_distribution_by_row_overview.png generated!')
