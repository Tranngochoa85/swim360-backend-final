from fastapi import APIRouter, HTTPException, status
from app.core.supabase_client import supabase
from app.api.v1.schemas.auth import UserCreate, UserLogin, Token
# Thay đổi duy nhất nằm ở dòng import này!
from gotrue.errors import AuthApiError

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate):
    """
    API endpoint để đăng ký tài khoản mới cho HLV.
    """
    try:
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
        })
        return {"message": "Registration successful! Please check your email to verify your account.", "user_id": response.user.id}
    # Và chúng ta cập nhật tên lỗi ở đây
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )

@router.post("/login", response_model=Token)
def login_for_access_token(user_data: UserLogin):
    """
    API endpoint để đăng nhập và nhận về access token.
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }
    # Và cả ở đây nữa
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )