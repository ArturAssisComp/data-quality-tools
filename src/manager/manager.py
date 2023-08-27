from pydantic import BaseModel
from manager.models.manager_arguments import ManagerArguments
## Tools:
# null value inspector
from tools.null_value_inspector.constants import CONSTANTS as NULL_VALUE_INSPECTOR_CONSTANTS
from tools.null_value_inspector.model.tool_arguments import ToolArguments as null_value_inspector_tool_arguments
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




class Manager:
    manager_arguments: ManagerArguments
    tool_arguments: BaseModel
    

    def process_user_request(self, raw_user_request: dict):
        self.manager_arguments = ManagerArguments(**raw_user_request)
        self._get_tool_arguments(raw_user_request)
        print(f'Manager arguments: {self.manager_arguments}')
        print(f'Tool arguments: {self.tool_arguments}')

        # TODO receive manager response from each tool
        # TODO create user response from manager response



    def _get_tool_arguments(self, raw_user_request: dict):
        tool_name = raw_user_request.get('tool_name')
        match raw_user_request.get('tool_name', None):
            case NULL_VALUE_INSPECTOR_CONSTANTS.tool_name | NULL_VALUE_INSPECTOR_CONSTANTS.alias:
                self.tool_arguments = null_value_inspector_tool_arguments(**raw_user_request)
            case None:
                raise ValueError('Tool name is required')
            case _:
                raise ValueError(f'Invalid tool name: {tool_name}')
        
