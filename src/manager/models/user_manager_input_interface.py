from pydantic import BaseModel

class Documentation (BaseModel):
    id: int
    name: str = 'doc'
    rules: dict[str, str] = dict()

class InputInterface (BaseModel):
    id: int
    name: str = ''
    description: str = ''
    dataset: list[str]
    documentation: Documentation
    tools_arguments: dict[str, list[str]]