from pydantic import BaseModel, field_validator

    
class Documentation (BaseModel):
    column:list[str]|None = None
    # TODO 3 - add is_subset_mode flag



    class Config:
        extra = "ignore"

    @field_validator('column')
    def validate_column(cls, v:list[dict]|None):
        if v is not None:
            if not v:
                raise ValueError('Empty documentation')
        return v
        


