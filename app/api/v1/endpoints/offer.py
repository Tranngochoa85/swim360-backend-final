from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.api.v1.dependencies import get_current_user, get_coach_profile_id
from app.api.v1.schemas.offer import OfferCreate, OfferResponse
from supabase import Client
from app.core.supabase_client import supabase
import json
from datetime import date, datetime
from uuid import UUID
from typing import List

def json_converter(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, UUID):
        return str(o)

router = APIRouter()

@router.post("/learning-requests/{request_id}/offers", status_code=status.HTTP_201_CREATED)
def create_offer_for_request(
    request_id: UUID,
    offer_data: OfferCreate,
    db: Client = Depends(lambda: supabase),
    coach_id: str = Depends(get_coach_profile_id)
):
    # ... (code cũ, giữ nguyên)
    request_res = db.table("learning_requests").select("id").eq("id", str(request_id)).eq("status", "pending").single().execute()
    if not request_res.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy yêu cầu học bơi hợp lệ.")
    offer_dict = offer_data.model_dump()
    offer_dict['coach_id'] = str(coach_id)
    offer_dict['learning_request_id'] = str(request_id)
    try:
        inserted_data = db.table("course_offers").insert(offer_dict).execute()
        if not inserted_data.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Không thể tạo ưu đãi.")
        json_compatible_data = json.dumps(inserted_data.data[0], default=json_converter)
        return Response(content=json_compatible_data, status_code=status.HTTP_201_CREATED, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# --- ENDPOINT MỚI CHO NGƯỜI HỌC ---

@router.get("/learning-requests/{request_id}/offers")
def get_offers_for_request(
    request_id: UUID,
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    """
    Lấy danh sách các ưu đãi cho một yêu cầu học bơi cụ thể.
    Chỉ chủ nhân của yêu cầu mới có quyền xem.
    """
    # Kiểm tra quyền sở hữu
    owner_res = db.table("learning_requests").select("user_id").eq("id", str(request_id)).single().execute()
    if not owner_res.data or owner_res.data['user_id'] != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền xem các ưu đãi này.")
    
    # Lấy danh sách ưu đãi
    offers_res = db.table("course_offers").select("*").eq("learning_request_id", str(request_id)).execute()
    
    json_compatible_data = json.dumps(offers_res.data, default=json_converter)
    return Response(content=json_compatible_data, media_type="application/json")

@router.post("/offers/{offer_id}/accept")
def accept_an_offer(
    offer_id: UUID,
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user) # Dependency get_current_user để Supabase biết auth.uid() là ai
):
    """
    Người học chấp nhận một ưu đãi.
    """
    try:
        # Gọi hàm 'accept_offer' trong database
        result = db.rpc('accept_offer', {'offer_id_to_accept': str(offer_id)}).execute()
        if not result.data:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể chấp nhận ưu đãi. Có thể ưu đãi không hợp lệ hoặc bạn không có quyền.")
        return {"message": "Ưu đãi đã được chấp nhận thành công!", "data": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))