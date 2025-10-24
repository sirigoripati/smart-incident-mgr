
from pydantic import BaseModel, AnyHttpUrl, Field
from typing import Optional
from datetime import datetime

class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    url: AnyHttpUrl
    expected_status: int = 200

class ServiceOut(BaseModel):
    id: int
    name: str
    url: AnyHttpUrl
    expected_status: int
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True

class IncidentOut(BaseModel):
    id: int
    service_id: int
    status_code: Optional[int]
    latency_ms: Optional[float]
    message: Optional[str]
    created_at: datetime
    resolved: bool
    resolved_at: Optional[datetime]
    class Config:
        orm_mode = True
