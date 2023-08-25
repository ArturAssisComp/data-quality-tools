from pydantic import BaseModel
from src.manager.models.documentation import Documentation
from src.manager.models.manager_arguments import ManagerArguments


class UserRequest (BaseModel):
    id: int
    name: str = ''
    description: str = ''
    dataset: list[str]
    documentation: Documentation
    manager_arguments: ManagerArguments
    tools_arguments: dict[str, list[str]]