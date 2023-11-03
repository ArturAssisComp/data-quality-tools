import logging
import json
import os

from pydantic import ValidationError

from tools.base_tool import  BaseToolClass
from tools.data_consistency_inspector.model.tool_arguments import ToolArguments
from tools.data_consistency_inspector.model.documentation import Documentation
from logger.utils import log_footer, log_header, get_custom_logger_name

from utils.file_operations import FileOperations

# tools

# snapshots
from tools.data_consistency_inspector.snapshot.row_inconsistency_distribution.row_inconsistency_distribution_snapshot import RowInconsistencyDistributionSnapshot

logger = logging.getLogger(get_custom_logger_name(__name__))



class DataConsistencyInspector(BaseToolClass):
    _row_inconsistency_distribution_snapshot_path:str|None
    _documentation:Documentation
    def __init__(self, logger:logging.Logger = logger, file_operations:FileOperations=FileOperations()):
        self._file_operations = file_operations
        self._logger = logger

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
        except FileNotFoundError as e:
            self._logger.info(f'No documentation provided: {e}')
            raise
        except ValidationError as e:
            self._logger.info(f'Invalid documentation: {e}')
            raise
        except Exception as e:
            self._logger.info(f'Error while reading documentation: {e}')
            raise
        return documentation
    

    def _create_snapshots(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_snapshot_path)
        log_header(logger, 'Initializing Snapshots')
        if self._row_inconsistency_distribution_snapshot_is_necessary(tool_arguments):
            try:
                rowInconsistencyDistributionSnapshot = RowInconsistencyDistributionSnapshot(self._documentation)
                rowInconsistencyDistributionSnapshot.create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._samples)
                self._row_inconsistency_distribution_snapshot_path = os.path.join(self._base_snapshot_path, rowInconsistencyDistributionSnapshot.get_filename())
            except Exception as e:
                self._logger.critical(e)
        log_footer(logger, 'Snapshots Finished    ')
    
    def _row_inconsistency_distribution_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return True


    def _create_results(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_result_path)
        log_header(logger, 'Initializing Results')
        log_footer(logger, 'Results Finished    ')
    



