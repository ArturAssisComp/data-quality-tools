from pydantic import BaseModel, field_validator

class Documentation (BaseModel):
    column:list[dict]|None = None



    class Config:
        extra = "ignore"

    @field_validator('column')
    def validate_column(cls, v:list[dict]|None):
        if v is not None:
            if any(map(lambda item: {'column', 'index'} != set(item.keys()), v)):
                raise ValueError('Invalid dictionary of columns')
        return v
        


