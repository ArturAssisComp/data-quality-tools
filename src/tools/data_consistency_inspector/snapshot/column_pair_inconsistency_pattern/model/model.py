from pydantic import   BaseModel


class ColumnPairInconsistencyPatternSnapshotContent(BaseModel):
    content:dict[str, dict[str, int]]


    