from pydantic import BaseModel, field_validator

    
class Documentation (BaseModel):
    column:list[str]|None = None



    class Config:
        extra = "ignore"

    @field_validator('column')
    def validate_column(cls, v:list[dict]|None):
        if v is not None:
            if not v:
                raise ValueError('Empty documentation')
        return v
        


