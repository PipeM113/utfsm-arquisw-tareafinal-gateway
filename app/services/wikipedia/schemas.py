from pydantic import BaseModel, Field


class ChatWikipediaRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)


class ChatWikipediaResponse(BaseModel):
    message: str
