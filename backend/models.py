from enum import Enum
from pydantic import BaseModel, Field, validator


class ToolEnum(Enum):
    WEB_SEARCH = "web-search"
    CALCULATOR = "calculator"


class Payload(BaseModel):
    prompt: str
    tool: ToolEnum

    @validator('prompt')
    def validate_prompt_length(cls, v):
        word_count = len(v)
        if word_count > 500:
            raise ValueError("Prompt must not exceed 500 words")
        return v