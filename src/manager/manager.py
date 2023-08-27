from typing import Type
from pydantic import BaseModel
from globals.interfaces import BaseToolClass
from manager.models.manager_arguments import ManagerArguments
import logging
## Tools:
# null value inspector
from tools.null_value_inspector.constants import CONSTANTS as NULL_VALUE_INSPECTOR_CONSTANTS
from tools.null_value_inspector.model.tool_arguments import ToolArguments as null_value_inspector_tool_arguments
from tools.null_value_inspector.null_value_inspector import NullValueInspector
'''
MANAGER 
- the manager will receive the user request and organize the response;
- each tool will generate a separate process;
- all the processes will only read the data, not write. This way, we do not need
to worry about race condition;
- each process will generate its results and send a message to the manager when
they are done;
- the manager will receive the messages and organize them for the response to the
final user;
'''
logger = logging.getLogger(__name__)




class Manager:
    manager_arguments: ManagerArguments
    tool_arguments: BaseModel
    tool_class: Type[BaseToolClass]
    

    def process_user_request(self, raw_user_request: dict):
        self._get_manager_arguments(raw_user_request)
        self._get_tool_arguments(raw_user_request)
        logger.info(f'Manager arguments: {self.manager_arguments}')
        logger.info(f'Tool arguments: {self.tool_arguments}')

        self._process_tool_request()

        # TODO receive manager response from each tool
        # TODO create user response from manager response



    def _process_tool_request(self):
        self.tool_class.work_on(self.tool_arguments)

    def _get_manager_arguments(self, raw_user_request: dict):
        self.manager_arguments = ManagerArguments(**raw_user_request)

    def _get_tool_arguments(self, raw_user_request: dict):
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
        
