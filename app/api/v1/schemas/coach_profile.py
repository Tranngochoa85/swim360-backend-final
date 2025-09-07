from pydantic import BaseModel, Field
from typing import List

# LƯU Ý: Đã loại bỏ Optional và giá trị mặc định None
class CoachProfileCreate(BaseModel):
    years_of_experience: int = Field(..., ge=0, description="Số năm kinh nghiệm, phải lớn hơn hoặc bằng 0")
    bio: str
    specializations: List[str]
    profile_link: str

class CoachProfileResponse(CoachProfileCreate):
    id: str
    user_id: str
    status: str

    class Config:
        from_attributes = True