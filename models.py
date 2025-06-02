from enum import Enum
from pydantic import BaseModel


class ToolEnum(Enum):
    WEB_SEARCH = "web-search"
    CALCULATOR = "calculator"


class Payload(BaseModel):
    prompt: str
    tool: ToolEnum