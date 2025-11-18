from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, model_validator


class DeviceEnum(str, Enum):
    web = "web"
    mobile = "mobile"
    desktop = "desktop"
    unknown = "unknown"


class StatusEnum(str, Enum):
    online = "online"
    offline = "offline"


class UserConnection(BaseModel):
    userId: str
    device: DeviceEnum = DeviceEnum.unknown
    ip: Optional[str] = None


class UserPresence(BaseModel):
    id: str
    userId: str
    device: DeviceEnum
    status: StatusEnum
    connectedAt: datetime
    lastSeen: datetime


class HealthResponse(BaseModel):
    status: str
    message: str


class PresenceRecordData(BaseModel):
    userId: str
    device: str
    status: str
    connectedAt: str
    lastSeen: str


class PresenceCreateResponse(BaseModel):
    status: str
    message: str
    data: PresenceRecordData


class PresenceListData(BaseModel):
    total_users: int
    users: List[UserPresence]


class PresenceListResponse(BaseModel):
    status: str
    message: str
    data: PresenceListData


class PresenceStatsData(BaseModel):
    total: int
    online: int
    offline: int


class PresenceStatsResponse(BaseModel):
    status: str
    message: str
    data: PresenceStatsData


class SinglePresenceResponse(BaseModel):
    status: str
    message: str
    data: UserPresence


class StatusUpdateRequest(BaseModel):
    status: Optional[StatusEnum] = None
    heartbeat: Optional[bool] = None

    @model_validator(mode='before')
    @classmethod
    def validate_status_or_heartbeat(cls, data: Any) -> Any:
        if isinstance(data, dict):
            status_val = data.get("status")
            heartbeat_val = data.get("heartbeat")

            if status_val is None and heartbeat_val is None:
                raise ValueError("Debe enviarse al menos 'status' o 'heartbeat'.")

            if status_val is not None and heartbeat_val is not None:
                raise ValueError("No se puede enviar 'status' y 'heartbeat' a la vez.")
        
        return data


class SimpleResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None 
