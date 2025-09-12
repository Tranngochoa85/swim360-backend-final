from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

# Các trường chung của một khóa học
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_type: str
    skill_level: str
    age_group: str
    price: float = Field(..., ge=0)
    total_sessions: int = Field(..., gt=0)
    session_duration: int = Field(..., gt=0)
    schedule_description: Optional[str] = None
    start_date: Optional[str] = None
    location_name: str
    location_address: Optional[str] = None
    max_students: int = Field(..., gt=0)
    status: str = 'draft' # Mặc định là bản nháp

# Dữ liệu API nhận vào khi tạo mới
class CourseCreate(CourseBase):
    pass

# Dữ liệu API nhận vào khi cập nhật (tất cả các trường đều không bắt buộc)
class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[str] = None
    # ... có thể thêm các trường khác nếu muốn cho phép cập nhật

# Dữ liệu API trả về
class CourseResponse(CourseBase):
    id: UUID
    coach_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True