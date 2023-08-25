import os
from pydantic import BaseModel, field_validator 


class ManagerArguments (BaseModel):
    name: str = ''
    description: str = ''
    dataset: list[str]
    output_path: str = ''

    @field_validator('dataset')
    def check_dataset(cls, v):
        for path in v:
            if not os.path.isfile(path):
                raise ValueError(f'{path} is not a valid path.')
        return v

    @field_validator('output_path')
    def check_output_path(cls, v):
        if v and not os.path.isdir(v):
            raise ValueError(f'{v} is not a valid path.')
        return v





