from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class MessageCreateIn(BaseModel):
    content: str
    type: Optional[str] = None
    paths: Optional[List[str]] = None


class MessageUpdateIn(BaseModel):
    content: Optional[str] = None
    paths: Optional[List[str]] = None


class MessageOut(BaseModel):
    id: UUID
    thread_id: UUID
    user_id: UUID
    type: Optional[str] = None
    content: Optional[str] = None
    paths: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MessagesPageOut(BaseModel):
    items: List[MessageOut]
    next_cursor: Optional[str] = None
    has_more: bool
