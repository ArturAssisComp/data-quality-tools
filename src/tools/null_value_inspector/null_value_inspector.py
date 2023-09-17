from globals.interfaces import BaseToolClass
from tools.null_value_inspector.model.tool_arguments import ToolArguments
import logging

logger = logging.getLogger(__name__)

class NullValueInspector(BaseToolClass):
    @classmethod
    def work_on(cls, tool_arguments: ToolArguments):
        print('Null Value Inspector initialized')
        print(f'{tool_arguments = }')
        print('Null Value Inspector finished')