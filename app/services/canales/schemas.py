from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ChannelType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class ChannelMember(BaseModel):
    id: str
    joined_at: float


class ErrorResponse(BaseModel):
    detail: str
    suggestion: Optional[str] = None


class Channel(BaseModel):
    id: Optional[str] = None
    name: str
    owner_id: str
    users: List[ChannelMember]
    is_active: bool
    channel_type: ChannelType
    created_at: float
    updated_at: float
    deleted_at: Optional[float] = None


class ChannelCreatePayload(BaseModel):
    name: str
    owner_id: str
    channel_type: ChannelType = ChannelType.PUBLIC


class ChannelUpdatePayload(BaseModel):
    name: Optional[str] = None
    owner_id: Optional[str] = None
    channel_type: Optional[ChannelType] = None


class ChannelBasicInfoResponse(BaseModel):
    id: str
    name: str
    owner_id: str
    channel_type: ChannelType
    created_at: float
    user_count: int


class ChannelIDResponse(BaseModel):
    id: str


class ChannelUserPayload(BaseModel):
    channel_id: str
    user_id: str
