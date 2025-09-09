from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time, datetime # Thêm datetime để xử lý created_at
from uuid import UUID

# Dữ liệu API nhận vào khi người dùng tạo yêu cầu (GIỮ NGUYÊN)
class LearningRequestCreate(BaseModel):
    course_type: str
    course_objective: str
    age_group: str
    sessions_per_week: int = Field(..., gt=0, le=8)
    preferred_days: List[str]
    preferred_time: time
    session_duration: int = Field(..., gt=0)
    num_adults: int = Field(default=0, ge=0)
    num_children: int = Field(default=0, ge=0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None

# Dữ liệu API trả về sau khi tạo thành công (CẬP NHẬT Ở ĐÂY)
class LearningRequestResponse(LearningRequestCreate):
    id: UUID
    user_id: UUID
    status: str
    
    # SỬA LỖI: Chuyển kiểu dữ liệu của trường trả về thành string
    # để khớp với định dạng có timezone của database
    preferred_time: str 
    
    created_at: datetime # Dùng datetime để xử lý tốt hơn

    class Config:
        from_attributes = True