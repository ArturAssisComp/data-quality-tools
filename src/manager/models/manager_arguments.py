import os
from pydantic import BaseModel, field_validator


class ManagerArguments (BaseModel):
    name: str = ''
    description: str = ''
    documentation: str = ''
    dataset: list[str]
    output_path: str = ''

    @field_validator('documentation')
    def check_documentation(cls, v):
        if v and not os.path.isfile(v):
            raise ValueError(f'{v} is not a valid path.')
        return v

    @field_validator('dataset', mode='before')
    def split_and_check_dataset(cls, v):
        if isinstance(v, str):  # Convert string to list
            v = v.split(',')
        for path in v:
            if not os.path.isfile(path) and not os.path.isdir(path):
                raise ValueError(f'{path} is not a valid path.')
        return v

    @field_validator('output_path')
    def check_output_path(cls, v):
        if v and not os.path.isdir(v):
            raise ValueError(f'{v} is not a valid path.')
        return v

    class Config:
        extra = "ignore" 
    

    





