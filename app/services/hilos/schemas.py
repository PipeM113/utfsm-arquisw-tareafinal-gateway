# app/services/hilos/schemas.py
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, constr


class ThreadStatus(str, Enum):
    OPEN = "open"
    ARCHIVED = "archived"


class ThreadCreate(BaseModel):
    channel_id: str
    title: constr(min_length=1, max_length=200)
    created_by: str
    meta: Optional[Dict[str, Any]] = None


class ThreadUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=200)] = None
    status: Optional[ThreadStatus] = None
    meta: Optional[Dict[str, Any]] = None


class ThreadOut(BaseModel):
    id: str
    channel_id: str
    title: str
    created_by: str
    status: ThreadStatus
    meta: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
