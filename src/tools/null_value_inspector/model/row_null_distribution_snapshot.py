from pydantic import BaseModel
from typing import Literal




class RowNullDistributionSnapshot(BaseModel):
    type:Literal['row_null_distribution_snapshot']
    files:list[str]
    content:dict[int, int]

    class Config:
        extra = 'forbid' 