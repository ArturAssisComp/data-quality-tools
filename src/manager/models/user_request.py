from pydantic import BaseModel
from src.manager.models.documentation import Documentation


class UserRequest (BaseModel):
    id: int
    name: str = ''
    description: str = ''
    dataset: list[str]
    documentation: Documentation
    tools_arguments: dict[str, list[str]]