from pydantic import  field_validator
from tools.null_value_inspector.snapshot.base_model import BaseSnapshotModel
from tools.null_value_inspector.snapshot.model.snapshot_model import BaseSnapshotContent


class RowNullDistributionSnapshotContent(BaseSnapshotContent):
    content:dict[int, int]

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v

    
    @classmethod
    def get_basic_instance(cls):
        new_instance = cls(content={0:0})
        new_instance.content = dict()
        return new_instance


class RowNullDistributionSnapshotModel(BaseSnapshotModel):
    content:dict[int, int]

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v

    
    @classmethod
    def get_basic_instance(cls):
        new_instance = cls(content={0:0}, type='row_null_distribution_snapshot')
        new_instance.content = dict()
        return new_instance