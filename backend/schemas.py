"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, HttpUrl


# Authentication Schemas
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class UserInfo(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[HttpUrl] = None


# Gmail Schemas
class EmailTask(BaseModel):
    task: str
    priority: Optional[str] = "medium"
    estimated_time: Optional[int] = None  # minutes


class EmailMessage(BaseModel):
    id: str
    subject: str
    sender: str
    date: str
    summary: str
    tasks: List[EmailTask] = []
    snippet: str
    labels: List[str] = []
    is_unread: bool = False


class EmailStats(BaseModel):
    unread_count: int
    today_count: int
    processed_today: int
    insights: List[str] = []
    productivity_tips: List[str] = []


class EmailSummaryResponse(BaseModel):
    messages: List[EmailMessage]
    total_count: int
    stats: EmailStats


# Drive Schemas
class DriveFile(BaseModel):
    id: str
    name: str
    mime_type: str
    size: Optional[str] = None
    modified_time: datetime
    web_view_link: Optional[HttpUrl] = None
    category: str
    confidence_score: Optional[float] = None


class DriveStats(BaseModel):
    storage_used: str
    storage_limit: str
    recent_files_count: int
    user_email: EmailStr
    insights: List[str] = []
    organization_score: Optional[int] = None


class DriveResponse(BaseModel):
    files: List[DriveFile]
    categories: Dict[str, List[DriveFile]]
    total_count: int
    category_summary: Dict[str, int]
    stats: DriveStats


# Calendar Schemas
class CalendarEvent(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    start: str
    end: str
    location: Optional[str] = None
    attendees: int = 0
    meeting_link: Optional[HttpUrl] = None
    event_type: Optional[str] = None  # meeting, focus, break


class FocusBlock(BaseModel):
    start: str
    end: str
    duration_hours: float
    suggestion: str
    block_type: str = "focus"


class CalendarStats(BaseModel):
    today_meetings: int
    week_meetings: int
    average_daily_meetings: float
    productivity_score: int
    insights: List[str] = []
    focus_time_available: float = 0.0


class CalendarResponse(BaseModel):
    events: List[CalendarEvent]
    total_events: int
    upcoming_today: List[CalendarEvent]
    focus_blocks: List[FocusBlock] = []
    stats: CalendarStats


# Dashboard Schemas
class DashboardStats(BaseModel):
    emails: EmailStats
    drive: DriveStats
    calendar: CalendarStats
    overall_productivity_score: int
    daily_summary: str
    recommendations: List[str] = []


# AI Processing Schemas
class SummarizationRequest(BaseModel):
    text: str
    max_length: int = 150
    min_length: int = 30


class SummarizationResponse(BaseModel):
    summary: str
    confidence_score: float
    processing_time: float


class TaskExtractionRequest(BaseModel):
    text: str
    max_tasks: int = 5


class TaskExtractionResponse(BaseModel):
    tasks: List[EmailTask]
    confidence_scores: List[float]
    processing_time: float


# Error Schemas
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.utcnow()


# Health Check Schema
class HealthCheck(BaseModel):
    status: str = "healthy"
    timestamp: datetime = datetime.utcnow()
    version: str = "1.0.0"
    services: Dict[str, str] = {}


# Pagination Schema
class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int