from pydantic import  BaseModel


class ColumnInconsistencyCountByTypeSnapshotContent(BaseModel):
    content:dict[str, dict[str, int]]

    

