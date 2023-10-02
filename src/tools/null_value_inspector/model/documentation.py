import os
from pydantic import BaseModel

class Documentation (BaseModel):
    column:list[dict]|None = None
    num_of_columns:int|None = None


    class Config:
        extra = "ignore"

