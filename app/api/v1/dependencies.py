from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.supabase_client import supabase
from gotrue.errors import AuthApiError
from supabase import Client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency để xác thực token và lấy thông tin người dùng hiện tại.
    """
    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- HÀM TRỢ GIÚP MỚI, DÙNG CHUNG ---
def get_coach_profile_id(
    current_user = Depends(get_current_user),
    db: Client = Depends(lambda: supabase)
) -> str:
    """
    Dependency để xác thực người dùng là một HLV đã được duyệt và trả về profile_id của họ.
    """
    user_id = current_user.id
    profile_res = db.table("coach_profiles").select("id").eq("user_id", str(user_id)).eq("status", "approved").single().execute()
    if not profile_res.data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hành động này yêu cầu quyền của Huấn Luyện Viên đã được duyệt.")
    return profile_res.data['id']