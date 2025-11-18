from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# --- PETICIONES ---

class ModerateMessageRequest(BaseModel):
    message_id: str
    user_id: str
    channel_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class AnalyzeTextRequest(BaseModel):
    text: str
    language: Optional[str] = None


class AddWordRequest(BaseModel):
    word: str
    language: str
    category: str
    severity: str
    is_regex: bool
    notes: Optional[str] = None


class UnbanUserRequest(BaseModel):
    channel_id: str
    reason: Optional[str] = None
    reset_strikes: bool = False


# --- RESPUESTAS GENERALES ---

class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


# --- RESPUESTAS DE MODERACIÓN DE MENSAJE / TEXTO ---

class ModerateMessageResponse(BaseModel):
    is_approved: bool
    action: str
    severity: str
    toxicity_score: float
    strike_count: int
    message: str
    detected_words: Optional[List[str]] = None
    language: Optional[str] = None
    ban_info: Optional[Dict[str, Any]] = None


class AnalyzeTextResponse(BaseModel):
    is_toxic: bool
    toxicity_score: float
    severity: str
    language: str
    detected_words: List[str]
    categories: List[str]
    detoxify_scores: Dict[str, float]


# --- ESTADO DE USUARIO / CANAL ---

class ModerationStatusResponse(BaseModel):
    user_id: str
    channel_id: str
    strike_count: int
    is_banned: bool
    ban_type: Optional[str] = None
    ban_expires_at: Optional[str] = None
    strikes_reset_at: Optional[str] = None
    last_violation: Optional[str] = None


# --- LISTA NEGRA (BLACKLIST) ---

class WordResponse(BaseModel):
    id: str
    word: str
    language: str
    category: str
    severity: str
    is_active: bool
    is_regex: bool
    added_by: Optional[str] = None
    added_at: str
    updated_at: str
    notes: Optional[str] = None


class BlacklistWordsResponse(BaseModel):
    total: int
    words: List[WordResponse]


class BlacklistStatsResponse(BaseModel):
    total: int
    active: int
    inactive: int
    by_language: Dict[str, int]
    by_category: Dict[str, int]
    by_severity: Dict[str, int]


# --- BANEOS Y VIOLACIONES ---

class BannedUserInfo(BaseModel):
    user_id: str
    channel_id: str
    ban_type: str
    banned_at: str
    banned_until: Optional[str] = None
    reason: str
    total_violations: int
    strike_count: int


class BannedUsersResponse(BaseModel):
    total: int
    banned_users: List[BannedUserInfo]


class ViolationInfo(BaseModel):
    id: str
    message_id: str
    detected_words: List[str]
    toxicity_score: float
    severity: str
    action_taken: str
    strike_count_at_time: int
    timestamp: str


class UserViolationsResponse(BaseModel):
    user_id: str
    channel_id: str
    total_violations: int
    current_strikes: int
    is_banned: bool
    violations: List[ViolationInfo]


class UserStatusResponse(BaseModel):
    user_id: str
    channel_id: str
    strike_count: int
    is_banned: bool
    ban_info: Optional[Dict[str, Any]] = None
    violation_summary: Dict[str, Any]


class ChannelStatsResponse(BaseModel):
    channel_id: str
    total_violations: int
    total_users_with_strikes: int
    banned_users: int
    temp_banned: int
    perm_banned: int
    avg_strikes: float
