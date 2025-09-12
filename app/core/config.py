from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Các biến môi trường cần thiết cho dự án
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    STRIPE_SECRET_KEY: str
    VNPAY_URL: str
    VNPAY_TMN_CODE: str
    VNPAY_HASH_SECRET: str
    VNPAY_RETURN_URL: str

    # THAY ĐỔI QUAN TRỌNG:
    # Thêm `extra='ignore'` để Pydantic bỏ qua các biến môi trường lạ không được định nghĩa ở trên.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()