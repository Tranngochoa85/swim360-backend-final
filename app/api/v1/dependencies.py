from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.supabase_client import supabase
from gotrue.errors import AuthApiError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency để xác thực token và lấy thông tin người dùng hiện tại.
    """
    try:
        # Dùng supabase client để xác thực token
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except AuthApiError as e:
        # Nếu token không hợp lệ, trả về lỗi 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )