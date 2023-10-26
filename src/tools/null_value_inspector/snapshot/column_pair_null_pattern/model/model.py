from pydantic import  field_validator, BaseModel


class ColumnPairNullPatternSnapshotContent(BaseModel):
    content:dict[str, dict[str, int]]

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v

    
    @classmethod
    def get_basic_instance(cls):
        new_instance = cls(content={'':dict()})
        new_instance.content = dict()
        return new_instance

