from pydantic import BaseModel, field_validator
from typing import Literal




class RowNullDistributionSnapshot(BaseModel):
    type:Literal['row_null_distribution_snapshot']
    files:list[str]
    content:dict[int, int]

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v

    class Config:
        extra = 'forbid' 