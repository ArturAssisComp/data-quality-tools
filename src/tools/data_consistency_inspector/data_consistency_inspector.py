import logging
import json

from tools.base_tool import  BaseToolClass
from tools.data_consistency_inspector.model.tool_arguments import ToolArguments
from tools.data_consistency_inspector.model.documentation import Documentation
from logger.utils import log_footer, log_header, get_custom_logger_name

from utils.file_operations import FileOperations

# tools

# snapshots

logger = logging.getLogger(get_custom_logger_name(__name__))



class DataConsistencyInspector(BaseToolClass):
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
        except Exception as e:
            logger.info(f'No documentation provided: {e}')
            documentation = Documentation(**dict())
        return documentation
    

    def _create_snapshots(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_snapshot_path)
        log_header(logger, 'Initializing Snapshots')
        log_footer(logger, 'Snapshots Finished    ')
    


    def _create_results(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_result_path)
        log_header(logger, 'Initializing Results')
        log_footer(logger, 'Results Finished    ')
    



