from pydantic import BaseModel



class Request(BaseModel):
    '''
    Each request is specific for a tool with a set of arguments
    '''
    id: int
    tool:str
    dataset: list[str]
    documentation: dict[str, str]
    arguments: list[str]

class ManagerRequest (BaseModel):
    '''
    Manager request is a set of requests to be executed by tools
    '''
    id: int
    name: str = ''
    description: str = ''
    requests: list[Request] 