from fastapi import FastAPI
# Thêm coach_profile vào dòng import
from app.api.v1.endpoints import auth, coach_profile

app = FastAPI(
    title="Swim360 API",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Swim360 API! The server is running correctly."}

# Gắn router xác thực
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

# Gắn router hồ sơ HLV
app.include_router(coach_profile.router, prefix="/api/v1/coach-profiles", tags=["Coach Profiles"])