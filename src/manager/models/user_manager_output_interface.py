from typing import Any
from pydantic import BaseModel, Json

class OutputInterface(BaseModel):
    id: int
    name: str = ''
    description: str = ''
    data_quality_snapshot: Json[Any] 
    data_quality_summary_report: Json[Any]
