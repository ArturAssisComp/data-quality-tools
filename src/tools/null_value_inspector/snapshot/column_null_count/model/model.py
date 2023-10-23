from pydantic import  field_validator
from tools.null_value_inspector.snapshot.base_model import BaseSnapshotModel
from tools.null_value_inspector.snapshot.model.snapshot_model import BaseSnapshotContent


class ColumnNullCountSnapshotContent(BaseSnapshotContent):
    content:dict[str, int]

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v

    
    @classmethod
    def get_basic_instance(cls):
        new_instance =  cls(content={'':0})
        new_instance.content = dict()
        return new_instance


class ColumnNullCountSnapshotModel(BaseSnapshotModel):
    content:dict[str, int]

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v

    
    @classmethod
    def get_basic_instance(cls):
        new_instance =  cls(content={'':0}, type='column_null_count_snapshot')
        new_instance.content = dict()
        return new_instance