from supabase import create_client, Client
from app.core.config import settings

# Khởi tạo kết nối đến Supabase sử dụng URL và key từ file config
supabase: Client = create_client(
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_ANON_KEY
)