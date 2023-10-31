from pydantic import BaseModel
from globals.types import SnapshotMode, SnapshotType 


class SnapshotModel(BaseModel):
    '''
    Model for snapshots. The snapshot's content is stored into either `samples` 
    or `population`. If no samples configuration were specified, it will be in
    `population`. It will be in `samples` otherwise.
    '''
    type:SnapshotType
    files:list[str] = list()
    state:SnapshotMode
    columns:list[str] = list()
    samples:dict[str, dict] | None = None
    population: dict | None = None
    

    class Config:
        extra = 'forbid' 
        use_enum_values = True