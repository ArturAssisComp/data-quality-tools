from typing import TypedDict, Callable, Any
from pydantic import BaseModel, field_validator

class Constraint(TypedDict):
    rule: Callable[[Any], bool]
    name: str

class Column(TypedDict):
    name: str
    type: str 
    constraints: list[Constraint]
    

class Documentation (BaseModel):
    columns:list[Column]|None = None
    is_subset_mode:bool = False

    class Config:
        extra = "ignore"

    @field_validator('columns')
    def validate_column(cls, v):
        if v is not None:
            if not v:
                raise ValueError('Empty documentation')
        return v
        


