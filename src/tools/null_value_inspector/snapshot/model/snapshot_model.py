from pydantic import BaseModel
import tools.null_value_inspector.snapshot.types as types
from globals.types import SnapshotType 


class BaseSnapshotContent(BaseModel):
    class Config:
        extra = 'forbid' 



class SnapshotModel(BaseModel):
    '''
    Model for snapshots. The snapshot's content is stored into either `samples` 
    or `population`. If no samples configuration were specified, it will be in
    `population`. It will be in `samples` otherwise.
    '''
    type:SnapshotType
    files:list[str] = list()
    state:types.State = 'initial'
    columns:list[str] = list()
    samples:dict[str, BaseSnapshotContent] | None = None
    population: BaseSnapshotContent | None = None
    

    class Config:
        extra = 'forbid' 
    