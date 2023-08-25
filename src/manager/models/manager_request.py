from pydantic import BaseModel
from src.manager.models.user_request import UserRequest
from src.manager.models.documentation import Documentation



class Request(BaseModel):
    '''
    Each request is specific for a tool with a set of arguments
    '''
    id: int
    tool:str
    dataset: list[str]
    documentation: Documentation
    arguments: list[str]

class ManagerRequest (BaseModel):
    '''
    Manager request is a set of requests to be executed by tools
    '''
    id: int
    name: str = ''
    description: str = ''
    requests: list[Request] 

    @classmethod
    def from_user_request(cls, user_request:UserRequest)->'ManagerRequest':
        managerRequestDict = {
            'id':user_request.id, 
            'name':user_request.name, 
            'description':user_request.description, 
            'requests':[]
        }
        for tool, arguments in user_request.tools_arguments.items():
            managerRequestDict['requests'].append({
                'id':user_request.id, 
                'tool':tool, 
                'dataset':user_request.dataset, 
                'documentation':user_request.documentation.model_dump(), 
                'arguments':arguments
            })
        return cls(**managerRequestDict)
