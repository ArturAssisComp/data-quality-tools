from pydantic import BaseModel

class Documentation (BaseModel):
    id: int
    name: str = 'doc'
    rules: dict[str, str] = dict()