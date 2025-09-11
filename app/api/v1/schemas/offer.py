from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# Dữ liệu API nhận vào khi HLV tạo ưu đãi
class OfferCreate(BaseModel):
    price: float = Field(..., ge=0, description="Mức học phí đề xuất")
    message: Optional[str] = None

# Dữ liệu API trả về sau khi tạo thành công
class OfferResponse(OfferCreate):
    id: UUID
    learning_request_id: UUID
    coach_id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True