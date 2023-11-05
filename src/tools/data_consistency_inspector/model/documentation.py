import re
from typing import Callable, Any
from pydantic import BaseModel, validator

from globals.types import ConsistencyCheckType

class RuleProcessor:
    @staticmethod
    def validate_rule(rule_str: str) -> bool:
        if not re.match(r"^[0-9a-zA-Z_ <>=&|()\[\].-]+$", rule_str):
            raise ValueError("Invalid characters in rule")
        return True

    @staticmethod
    def create_rule(rule_str: str) -> Callable[[Any], bool]:
        RuleProcessor.validate_rule(rule_str)
        return eval(f"lambda x: {rule_str}", {}, {})


class Constraint(BaseModel):
    rule: Callable[[Any], bool] | None
    name: str 

    class Config:
        extra = 'forbid' 

    @validator("rule", pre=True)
    def validate_rule(cls, v):
        if isinstance(v, str):
            return RuleProcessor.create_rule(v)
        return v

class Column(BaseModel):
    name: str
    data_type: ConsistencyCheckType 
    type_size:int|None = None
    constraints: list[Constraint] = list()

    @validator("data_type", pre=True)
    def validate_columns(cls, v:str):
        if v.islower():
            v = v.upper()
            match v[:2]:
                case 'SS':
                    v = 'ss' + v[2:]
        return v
    
    @validator("type_size")
    def validate_type_size(cls, v:int|None):
        if v is not None and v <= 0:
            raise ValueError('type_size must be positive')
        return v



    class Config:
        extra = 'forbid' 

class Documentation(BaseModel):
    columns: list[Column] | None = None
    is_subset_mode: bool = False

    @validator("columns", pre=True)
    def validate_columns(cls, v):
        if not v:
            raise ValueError("Empty documentation")
        return v
