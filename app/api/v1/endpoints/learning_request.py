from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.api.v1.dependencies import get_current_user, get_coach_profile_id # Sửa lại import
from app.api.v1.schemas.learning_request import LearningRequestCreate, LearningRequestResponse
from supabase import Client
from app.core.supabase_client import supabase
from typing import List
import json
from datetime import date, datetime
from uuid import UUID

def json_converter(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, UUID):
        return str(o)

router = APIRouter()

# ... (Hàm create_learning_request không đổi) ...
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_learning_request(
    request_data: LearningRequestCreate,
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    request_dict = request_data.model_dump()
    request_dict['user_id'] = str(user_id)
    request_dict['preferred_time'] = request_data.preferred_time.isoformat()
    try:
        inserted_data = db.table("learning_requests").insert(request_dict).execute()
        if not inserted_data.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Không thể tạo yêu cầu học bơi.")
        
        json_compatible_data = json.dumps(inserted_data.data[0], default=json_converter)
        return Response(content=json_compatible_data, status_code=status.HTTP_201_CREATED, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Endpoint cho HLV (không đổi)
@router.get("/discover")
def discover_learning_requests(
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    get_coach_profile_id(current_user, db) # Sửa lại cách gọi hàm
    try:
        requests_res = db.table("learning_requests").select("*").eq("status", "pending").execute()
        json_compatible_data = json.dumps(requests_res.data, default=json_converter)
        return Response(content=json_compatible_data, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# --- ENDPOINT MỚI CHO NGƯỜI HỌC ---
@router.get("/my-requests")
def get_my_learning_requests(
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    """
    Lấy danh sách các yêu cầu học bơi do chính người dùng hiện tại tạo.
    """
    try:
        # Lọc các yêu cầu có user_id khớp với id của người dùng đang đăng nhập
        requests_res = db.table("learning_requests").select("*").eq("user_id", str(current_user.id)).execute()
        
        json_compatible_data = json.dumps(requests_res.data, default=json_converter)
        return Response(content=json_compatible_data, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))