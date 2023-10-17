from pydantic import BaseModel, field_validator
import tools.null_value_inspector.snapshot.types as types




class BaseSnapshotModel(BaseModel):
    type:types.Snapshot  
    files:list[str] = list()
    state:types.State = 'initial'
    num_of_columns:int|None = None

    
    @field_validator('num_of_columns')
    def num_of_column_validator(cls, v):
        if v and v <= 0:
            raise ValueError(f'num_of_columns ({v}) must be positive')
        return v

    class Config:
        extra = 'forbid' 
    
    @classmethod
    def get_basic_instance(cls):
        raise NotImplementedError('must implement')