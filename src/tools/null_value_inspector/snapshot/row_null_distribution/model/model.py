from pydantic import BaseModel, field_validator
import tools.null_value_inspector.snapshot.row_null_distribution.types as types




class RowNullDistributionSnapshotModel(BaseModel):
    type:types.RowNullDistributionSnapshot = 'row_null_distribution_snapshot' 
    files:list[str] = list()
    content:dict[int, int]
    state:types.State = 'initial'
    num_of_columns:int|None = None

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v
    
    @field_validator('num_of_columns')
    def num_of_column_validator(cls, v):
        if v and v <= 0:
            raise ValueError(f'num_of_columns ({v}) must be positive')
        return v

    class Config:
        extra = 'forbid' 
    
    @classmethod
    def get_basic_instance(cls):
        return cls(content={0:0})