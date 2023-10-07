from pydantic import BaseModel, field_validator
from typing import Literal


ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE:Literal['row_null_distribution_snapshot'] = 'row_null_distribution_snapshot'


class RowNullDistributionSnapshotModel(BaseModel):
    type:Literal['row_null_distribution_snapshot'] = ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE
    files:list[str] = list()
    content:dict[int, int]
    state:Literal['initial', 'free-mode', 'strict-mode'] = 'initial'
    num_of_columns:int|None = None

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v

    class Config:
        extra = 'forbid' 
    
    @classmethod
    def get_basic_instance(cls):
        return cls(content={0:0})