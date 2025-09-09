from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.dependencies import get_current_user
from app.api.v1.schemas.learning_request import LearningRequestCreate, LearningRequestResponse
from supabase import Client
from app.core.supabase_client import supabase

router = APIRouter()

@router.post("/", response_model=LearningRequestResponse, status_code=status.HTTP_201_CREATED)
def create_learning_request(
    request_data: LearningRequestCreate,
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    """
    Tạo một "Yêu cầu học bơi" mới. Yêu cầu người dùng phải đăng nhập.
    """
    user_id = current_user.id
    
    # Chuyển đổi Pydantic model thành dictionary để insert
    request_dict = request_data.model_dump()
    # Thêm user_id của người dùng đang đăng nhập vào
    request_dict['user_id'] = str(user_id)
    # Chuyển đổi time object thành string theo định dạng ISO 8601
    request_dict['preferred_time'] = request_data.preferred_time.isoformat()

    try:
        # Chèn dữ liệu vào bảng learning_requests
        inserted_data = db.table("learning_requests").insert(request_dict).execute()
        
        if not inserted_data.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Không thể tạo yêu cầu học bơi.")
            
        return inserted_data.data[0]

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))