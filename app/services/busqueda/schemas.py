# app/services/busqueda/schemas.py
from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel


class IndexEnum(str, Enum):
    ALL = "all"
    MESSAGES = "messages"
    THREADS = "threads"
    FILES = "files"


class SearchHit(BaseModel):
    index: str
    id: str
    source: Dict[str, Any]


class SearchResponse(BaseModel):
    total: int
    results: List[SearchHit]
