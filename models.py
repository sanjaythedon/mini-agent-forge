from typing import Literal
from pydantic import BaseModel


class Payload(BaseModel):
    WEB_SEARCH = "web-search"
    CALCULATOR = "calculator"

    prompt: str
    tool: Literal[WEB_SEARCH, CALCULATOR]