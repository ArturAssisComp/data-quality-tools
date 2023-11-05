from pydantic import  field_validator, BaseModel


class RowInconsistencyDistributionSnapshotContent(BaseModel):
    content:dict[int, int]

    @field_validator('content')
    def content_validator(cls, v):
        if(len(v) == 0):
            raise ValueError('Content must not be empty.')
        return v
    

