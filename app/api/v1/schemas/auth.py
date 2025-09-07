from pydantic import BaseModel, EmailStr

# Dữ liệu cần thiết để tạo tài khoản
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Dữ liệu cần thiết để đăng nhập
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Dữ liệu trả về sau khi đăng nhập thành công
class Token(BaseModel):
    access_token: str
    token_type: str