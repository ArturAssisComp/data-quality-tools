import logging
import os
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
FIG_NAME = 'abs_ranked_inconsistency_count_by_type_and_column_overview.png'
Y_LABEL = 'Inconsistencies Count'
X_LABEL = 'Inconsistency Per Column'
TITLE = 'Ranked Inconsistency Count by Column and Type Overview'


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
        except Exception as e:
            self._logger.error(f'Result not generated: {e}')





    

    def _generate_bar_plot(self, content: dict, basedir_path: str, name_prefix: str=''):
        """
        Generates a bar plot from the given content and saves it to a specified directory.

        Parameters:
        content (dict): A dictionary of main groups with subgroups as keys and their values.
        basedir_path (str): The base directory path where the plot will be saved.
        name_prefix (str): Optional prefix for the saved plot filename.
        """
        # Flatten the content into a list of (main_group, sub_group, value) tuples, excluding zero values
        flat_content = [(main_group, sub_group, value) 
                        for main_group, subgroups in content.items()
                        for sub_group, value in subgroups.items() if value != 0]

        # Sort and get unique subgroups across all main groups
        all_subgroups = sorted({sub_group for _, sub_group, _ in flat_content}, )

        # Start plotting
        fig, ax = plt.subplots()
        group_positions = []  # Store the x position for each main group
        subgroup_labels = []  # Store the x position and label for each subgroup

        current_position = 0  # Start at position 0 on the x-axis

        # Go through each main group and its subgroups
        for sub_content in content.values():
            # Sort subgroups by the order in all_subgroups
            subgroups = sorted(((k, v) for k, v in sub_content.items() if v != 0), key=lambda item: all_subgroups.index(item[0]), reverse=True)

            # Calculate width for each subgroup bar
            num_subgroups = len(subgroups)
            width_per_subgroup = 0.8 / max(len(all_subgroups), num_subgroups) if num_subgroups else 0.8
            subgroup_start_position = current_position - (0.8 / 2) + (width_per_subgroup / 2)

            # Plot each subgroup
            for i, (sub_group, value) in enumerate(subgroups):
                x_position = subgroup_start_position + i * width_per_subgroup
                ax.bar(x_position, value, width_per_subgroup, label=sub_group if not group_positions else "", align='center')
                subgroup_labels.append((x_position, sub_group))

            group_positions.append(current_position)
            current_position += 1

        # Set the x-axis labels for subgroups and groups
        self._set_axis_labels(ax, group_positions, subgroup_labels, content.keys())

        # Add the y-axis label and title
        ax.set_ylabel(Y_LABEL)
        ax.set_title(TITLE)


        # Save the plot
        self._save_plot(fig, basedir_path, name_prefix)

    def _set_axis_labels(self, ax, group_positions, subgroup_labels, group_labels):
        """
        Sets the axis labels for the plot.
        """
        ax.set_xticks([pos for pos, label in subgroup_labels])
        ax.set_xticklabels([label for pos, label in subgroup_labels], rotation=45, ha="right")

        # Create a second x-axis for the main group labels
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(group_positions)
        ax2.set_xticklabels(group_labels)
        ax2.xaxis.set_ticks_position('bottom')
        ax2.xaxis.set_label_position('bottom')
        ax2.spines['bottom'].set_position(('outward', 40))
        ax2.tick_params(axis='x', which='major', pad=15)

    def _save_plot(self, fig, basedir_path, name_prefix):
        """
        Saves the plot to the specified directory.
        """
        filename = f'{name_prefix}{FIG_NAME}'
        fig_path = os.path.join(basedir_path, filename)
        plt.tight_layout()
        plt.savefig(fig_path, bbox_inches='tight')
        plt.close(fig)
        self._logger.info(f'{FIG_NAME} generated!')