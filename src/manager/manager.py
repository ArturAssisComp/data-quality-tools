from typing import Type
import logging

from tools.base_tool import BaseToolClass
from tools.base_tool_arguments import BaseToolArguments
from manager.models.manager_arguments import ManagerArguments
from logger.utils import get_custom_logger_name
## Tools:
# null value inspector
from tools.null_value_inspector.constants import CONSTANTS as NULL_VALUE_INSPECTOR_CONSTANTS
from tools.null_value_inspector.model.tool_arguments import ToolArguments as null_value_inspector_tool_arguments
from tools.null_value_inspector.null_value_inspector import NullValueInspector

logger = logging.getLogger(get_custom_logger_name(__name__))




class Manager:
    manager_arguments: ManagerArguments
    tool_arguments: BaseToolArguments
    tool_class: Type[BaseToolClass]
    

    def process_user_request(self, raw_user_request: dict):
        try:
            self._get_manager_arguments(raw_user_request)
            self._get_tool_arguments(raw_user_request)
        except Exception as e:
            logger.error(f'Error while reading arguments: {e}')
            raise
        self._process_tool_request()


    def _process_tool_request(self):
        self.tool_class().work_on(self.tool_arguments)

    def _get_manager_arguments(self, raw_user_request: dict):
        self.manager_arguments = ManagerArguments(**raw_user_request)

    def _get_tool_arguments(self, raw_user_request: dict):
        """Determine which tool the user is requesting and set the appropriate arguments and class."""
        tool_name = raw_user_request.get('tool_name')
        match raw_user_request.get('tool_name', None):
            case NULL_VALUE_INSPECTOR_CONSTANTS.tool_name | NULL_VALUE_INSPECTOR_CONSTANTS.alias:
                self.tool_arguments = null_value_inspector_tool_arguments(**raw_user_request)
                self.tool_class = NullValueInspector
            case None:
                logger.error('Tool name is required')
                raise ValueError
            case _:
                logger.error(f'Invalid tool name: {tool_name}')
                raise ValueError
        
