from pydantic import BaseModel
import tools.null_value_inspector.snapshot.types as types




class BaseSnapshotModel(BaseModel):
    type:types.Snapshot  
    files:list[str] = list()
    state:types.State = 'initial'

    

    class Config:
        extra = 'forbid' 
    
    @classmethod
    def get_basic_instance(cls):
        raise NotImplementedError('must implement')