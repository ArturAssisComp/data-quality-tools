from pydantic import BaseModel

class ToolArguments (BaseModel):
    tool_name: str

    class Config:
        extra = "ignore"