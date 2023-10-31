import logging
import os
from pydantic import BaseModel

from globals.constants import CONSTANTS
from logger.utils import get_custom_logger_name
from tools.base_tool_arguments import BaseToolArguments
from utils.file_operations import FileOperations
from utils.str_operations import parse_samples

logger = logging.getLogger(get_custom_logger_name(__name__))

class BaseToolClass:
    _base_snapshot_path:str
    _base_result_path:str 
    _documentation:BaseModel
    _file_operations:FileOperations
    _logger:logging.Logger
    _samples:list[str | int] | None
    def __init__(self, logger:logging.Logger = logger, file_operations:FileOperations=FileOperations()):
        self._file_operations = file_operations
        self._logger = logger

    def work_on(self, tool_arguments: BaseToolArguments):
        self._base_snapshot_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.snapshot)
        self._base_result_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.results)
        documentation_path = tool_arguments.documentation

        self._documentation = self._get_documentation(documentation_path)

        # parse samples
        self._samples = self._get_samples_specification(tool_arguments.sample)

        # create the snapshots
        self._create_snapshots(tool_arguments)

        # create the results
        self._create_results(tool_arguments)


    def _get_documentation(self, documentation_path:str):
        """
        Retrieves the documentation from the provided path.
        """
        raise NotImplementedError('should implement')

    def _create_snapshots(self, tool_arguments:BaseToolArguments):
        raise NotImplementedError('should implement')


    def _create_results(self, tool_arguments:BaseToolArguments):
        raise NotImplementedError('should implement')


    def _get_samples_specification(self, sample_arg:str):
        if sample_arg:
            try:
                result =  parse_samples(sample_arg)
                if result:
                    return result
                raise ValueError('Empty result')
            except Exception as e:
                logger.error(f'Invalid argument samples ({sample_arg}): {e}')
                raise
        else:
            return None


    def _snapshot_is_available(self, snapshot_path:str|None):
        return snapshot_path and os.path.isfile(snapshot_path)