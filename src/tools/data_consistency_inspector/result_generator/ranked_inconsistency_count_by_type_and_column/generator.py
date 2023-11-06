import logging
import os
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
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
        'fig_name': 'rel_ranked_inconsistency_count_by_type_and_column_overview.png',
        'suffix': '%'
    },
    'absolute': {
        'y_label': 'Row Count',
        'fig_name': 'abs_ranked_inconsistency_count_by_type_and_column_overview.png',
        'suffix': ''
    }
}
CONTENT_SIZE_LIMIT_FOR_TOP_LABEL = 20
CONTENT_SIZE_LIMIT_FOR_X_LABEL = 50
VALUE_SIZE_LIMIT = 1000
X_LABEL = 'Inconsistency Per Column'
TITLE = 'Ranked Inconsistency Count by Column Overview'


class RankedInconsistencyCountByTypeAndColumnOverviewGenerator(BaseOverviewGenerator):
    _plot_operations:PlotOperations
    _needed_snapshots:list[SnapshotType] = [SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT]
    def __init__(self,snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations(), plot_operations:PlotOperations=PlotOperations()):
        super().__init__(snapshot_filepath, logger=logger, fileOperations=fileOperations)
        self._plot_operations = plot_operations
    
    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        column_inconsistency_count_by_type_snapshot_content:ColumnInconsistencyCountByTypeSnapshotContent = parsed_content_dict[SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT]

        try:
            try:
                self._generate_bar_plot(column_inconsistency_count_by_type_snapshot_content.content, basedir_path, name_prefix=name_preffix)
            finally:
                plt.close()
            try:
                self._generate_bar_plot(column_inconsistency_count_by_type_snapshot_content.content, basedir_path, relative=True, name_prefix=name_preffix)
            finally:
                plt.close()
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')


    def _should_add_label_on_top(self, content:dict, relative:bool):
        basic_check = len(content) <= CONTENT_SIZE_LIMIT_FOR_TOP_LABEL 
        if relative:
            return basic_check
        return basic_check and max(content.values()) < VALUE_SIZE_LIMIT

    '''
    # TODO refactor: extract this function, because it is implemented also in null value inspector tool
    def _generate_bar_plot(self,column_inconsistency_count_snapshot_content:ColumnInconsistencyCountByTypeSnapshotContent, basedir_path:str, name_preffix:str='', relative:bool=False):
        content = column_inconsistency_count_snapshot_content.content

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
    '''


    def _generate_bar_plot(self, content: dict, basedir_path: str, name_prefix: str='', relative: bool=False):
            groups = []
            group_values = {}

            # Collect all subgroups with non-zero values and their sums across groups
            for group, sub_content in content.items():
                groups.append(group)
                for sub_group, value in sub_content.items():
                    if value != 0:  # Exclude subgroups with zero value
                        if sub_group not in group_values:
                            group_values[sub_group] = []
                        group_values[sub_group].append((group, value))

            # Sort subgroups by the sum of their values
            sorted_sub_groups = sorted(group_values, key=lambda x: sum(val for _, val in group_values[x]), reverse=True)

            # Create a figure and a set of subplots
            fig, ax = plt.subplots()

            # Calculate the bar positions
            num_groups = len(groups)
            total_width = 0.8  # Total width for all bars in one group
            bar_width = total_width / len(sorted_sub_groups)

            for i, sub_group in enumerate(sorted_sub_groups):
                sub_group_data = group_values[sub_group]
                sub_group_data.sort(key=lambda x: groups.index(x[0]))  # Sort by the group order
                x = np.arange(num_groups)
                heights = [0] * num_groups  # Start with zero heights for each group
                
                for group, value in sub_group_data:
                    group_index = groups.index(group)
                    heights[group_index] = value

                offsets = (i - len(sorted_sub_groups) / 2) * bar_width + bar_width / 2
                ax.bar(x + offsets, heights, bar_width, label=sub_group)

            # Add some text for labels, title, and custom x-axis tick labels
            ax.set_xlabel('Groups')
            ax.set_ylabel('Values')
            ax.set_title('Your Title Here')
            ax.set_xticks(x)
            ax.set_xticklabels(groups, rotation=45)
            ax.legend()

            # Save the plot
            filename = f"{name_prefix}bar_plot.png"
            fig_path = os.path.join(basedir_path, filename)
            plt.savefig(fig_path, bbox_inches='tight')
            plt.close(fig)  # Close the figure to free memory
            
            self._logger.info(f'Bar plot generated at {fig_path}!')



