from typing import Any
from pydantic import BaseModel, Json

class Response(BaseModel):
    '''
    Each response stores the result of the application of a tool
    '''
    id: int
    tool:str
    dataset: list[str]
    data_quality_snapshot: Json[Any] 
    data_quality_summary_report: Json[Any]

class ManagerResponse (BaseModel):
    id: int
    name: str = ''
    description: str = ''
    responses: list[Response] 