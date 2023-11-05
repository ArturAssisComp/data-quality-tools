from pydantic import  BaseModel


class ColumnNullCountSnapshotContent(BaseModel):
    content:dict[str, int]
