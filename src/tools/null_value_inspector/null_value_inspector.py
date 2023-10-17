import os
import logging
import json

from globals.interfaces import BaseToolClass
from globals.constants import CONSTANTS
from tools.null_value_inspector.model.tool_arguments import ToolArguments
from tools.null_value_inspector.model.documentation import Documentation
from logger.utils import log_footer, log_header, get_custom_logger_name

# tools
from tools.null_value_inspector.result_generator.null_distribution_by_row.generator import NullDistributionByRowOverviewGenerator
from tools.null_value_inspector.result_generator.statistical_summary.generator import StatisticalSummaryOverviewGenerator

# snapshots
from tools.null_value_inspector.snapshot.row_null_distribution.row_null_distribution_snapshot import RowNullDistributionSnapshot
from utils.file_operations import FileOperations

logger = logging.getLogger(get_custom_logger_name(__name__))



class NullValueInspector(BaseToolClass):
    _row_null_distribution_snapshot_path:str | None
    _base_snapshot_path:str
    _base_result_path:str 
    _documentation:Documentation
    _file_operations:FileOperations
    def __init__(self, file_operations:FileOperations=FileOperations()):
        self._row_null_distribution_snapshot_path = None
        self._file_operations = file_operations


    def work_on(self, tool_arguments: ToolArguments):
        self._base_snapshot_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.snapshot)
        self._base_result_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.results)
        documentation_path = tool_arguments.documentation

        self._documentation = self._get_documentation(documentation_path)

        # create the snapshots
        self._create_snapshots(tool_arguments)

        # create the results
        self._create_results(tool_arguments)


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
    

    def _create_snapshots(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_snapshot_path)
        log_header(logger, 'Initializing Snapshots')
        if self._row_null_distribution_snapshot_is_necessary(tool_arguments):
            rowNullDistributionSnapshot = RowNullDistributionSnapshot()
            rowNullDistributionSnapshot.create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._documentation)
            self._row_null_distribution_snapshot_path = os.path.join(self._base_snapshot_path, rowNullDistributionSnapshot.get_filename())

        log_footer(logger, 'Snapshots Finished    ')

    def _row_null_distribution_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.null_distribution_by_row_overview or tool_arguments.statistical_summary_overview

    def _create_results(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_result_path)
        log_header(logger, 'Initializing Results')
        if tool_arguments.statistical_summary_overview:
            logger.info('Creating summary_overview')
            if not self._snapshot_is_available(self._row_null_distribution_snapshot_path):
                logger.error('Invalid row_null_distribution_snapshot')
            else:
                StatisticalSummaryOverviewGenerator().generate_overview(self._row_null_distribution_snapshot_path, self._base_result_path, self._documentation) # type: ignore
        if tool_arguments.null_distribution_by_row_overview:
            logger.info('Creating null_distribution_by_row_overview')
            if not self._snapshot_is_available(self._row_null_distribution_snapshot_path):
                logger.error('Invalid row_null_distribution_snapshot')
            else:
                NullDistributionByRowOverviewGenerator().generate_overview(self._row_null_distribution_snapshot_path, self._base_result_path) # type: ignore
        log_footer(logger, 'Results Finished    ')
    
    def _snapshot_is_available(self, snapshot_path:str|None):
        return snapshot_path and os.path.isfile(snapshot_path)


