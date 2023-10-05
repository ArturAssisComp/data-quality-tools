import os
import logging
import json

from globals.interfaces import BaseToolClass
from globals.constants import CONSTANTS
from tools.null_value_inspector.model.tool_arguments import ToolArguments
from tools.null_value_inspector.model.documentation import Documentation
from tools.null_value_inspector.snapshot.row_null_distribution.row_null_distribution_snapshot import RowNullDistributionSnapshot
from logger.utils import log_footer, log_header, get_custom_logger_name

logger = logging.getLogger(get_custom_logger_name(__name__))



class NullValueInspector(BaseToolClass):
    def _get_documentation(self, documentation_path:str):
        """
        Retrieves the documentation from the provided path.
        """
        try:
            with open(documentation_path, 'r') as f:
                # Load JSON data from file
                data = json.load(f)
                documentation = Documentation(**data)
                logger.info(f'Documentation read: {documentation}')
        except Exception as e:
            logger.info(f'No documentation provided: {e}')
            documentation = Documentation(**dict())
        return documentation
    
    def _create_snapshot_directory(self, snapshot_path:str):
        try:
            if not os.path.isdir(snapshot_path):
                os.makedirs(snapshot_path)
        except Exception as e:
            logger.error(f'Not able to create directories for snapshot path: {e}')
            raise

    def _row_null_distribution_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.null_distribution_by_row_overview

    def _create_snapshots(self, tool_arguments:ToolArguments, snapshot_path:str, documentation:Documentation):
        log_header(logger, 'Initializing Snapshots')
        if self._row_null_distribution_snapshot_is_necessary(tool_arguments):
            self._create_snapshot_directory(snapshot_path)
            RowNullDistributionSnapshot().create_row_null_distribution_snapshot(tool_arguments.dataset, snapshot_path, documentation)

        log_footer(logger, 'Snapshots Finished    ')

    
    def _create_results(self, tool_arguments:ToolArguments):
        log_header(logger, 'Initializing Results')
        if tool_arguments.null_distribution_by_row_overview:
            logger.info('Creating null-distribution-by-row-overview')

        log_footer(logger, 'Results Finished    ')


    def work_on(self, tool_arguments: ToolArguments):
        snapshot_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.snapshot)
        documentation_path = tool_arguments.documentation

        documentation = self._get_documentation(documentation_path)

        # create the snapshots
        self._create_snapshots(tool_arguments, snapshot_path, documentation)

        # create the results
        self._create_results(tool_arguments)
    




