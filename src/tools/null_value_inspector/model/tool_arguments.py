import os
from pydantic import BaseModel, field_validator

class ToolArguments (BaseModel):
    tool_name: str
    documentation: str = ''
    dataset: list[str]
    output_path: str = ''
    ranked_null_count_by_column_overview:bool = False
    null_distribution_by_row_overview:bool = False
    statistical_summary_overview:bool = False



    @field_validator('dataset', mode='before')
    def split_and_check_dataset(cls, v):
        if isinstance(v, str):  # Convert string to list
            v = list(map(str.strip, v.split(',')))
            for path in v:
                if not os.path.isfile(path) and not os.path.isdir(path):
                    raise ValueError(f'{path} is not a valid path.')
        else:
            raise TypeError('Expected str type')
        return v

    @field_validator('output_path')
    def check_output_path(cls, v):
        if v and not os.path.isdir(v):
            raise ValueError(f'{v} is not a valid path.')
        return v

    class Config:
        extra = "ignore"

