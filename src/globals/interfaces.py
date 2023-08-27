from pydantic import BaseModel

class BaseToolClass:
    @classmethod
    def work_on(cls, tool_arguments: BaseModel):
        raise NotImplementedError('This method must be implemented')