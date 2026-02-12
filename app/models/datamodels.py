from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = Field(default=True)

class Printer(BaseModel):
    id: str
    name: str
    status: str
    ip_address: Optional[str] = None
    printer_type: Optional[str] = None
    in_service: bool = Field(default=True)

class PrintJob(BaseModel):
    id: int
    printer_id: int
    user_id: int
    file_name: str
    status: str
    progress: float = Field(ge=0.0, le=100.0)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

