from enum import Enum
from pydantic import BaseModel, Field


class ToolEnum(Enum):
    WEB_SEARCH = "web-search"
    CALCULATOR = "calculator"


class Payload(BaseModel):
    prompt: str = Field(..., max_length=500)
    tool: ToolEnum