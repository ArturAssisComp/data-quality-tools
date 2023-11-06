from pydantic import  BaseModel


class ColumnPairNullPatternSnapshotContent(BaseModel):
    content:dict[str, dict[str, int]]

