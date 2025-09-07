from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.dependencies import get_current_user
from app.api.v1.schemas.coach_profile import CoachProfileCreate, CoachProfileResponse
from supabase import Client
from app.core.supabase_client import supabase
from pydantic import UUID4

router = APIRouter()

@router.post("/", response_model=CoachProfileResponse, status_code=status.HTTP_201_CREATED)
def create_coach_profile(
    profile_data: CoachProfileCreate,
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    """
    Tạo một hồ sơ HLV mới. Yêu cầu người dùng phải đăng nhập.
    """
    # Lấy user_id từ token đã được xác thực
    user_id = current_user.id
    
    # 1. Kiểm tra xem user này đã có profile chưa
    existing_profile = db.table("coach_profiles").select("id").eq("user_id", user_id).execute()
    if existing_profile.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Coach profile already exists for this user.")

    # 2. Tạo đối tượng dữ liệu để chèn vào DB
    profile_to_insert = profile_data.model_dump()
    profile_to_insert['user_id'] = str(user_id) # Chuyển UUID thành string

    # 3. Chèn vào database
    try:
        inserted_profile = db.table("coach_profiles").insert(profile_to_insert).execute()
        
        if not inserted_profile.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create coach profile.")
            
        # Supabase v2 trả về một list, ta lấy phần tử đầu tiên
        created_profile = inserted_profile.data[0]
        
        # Chuyển đổi ID về dạng string để response model hoạt động đúng
        created_profile['id'] = str(created_profile['id'])
        created_profile['user_id'] = str(created_profile['user_id'])
        
        return created_profile

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))