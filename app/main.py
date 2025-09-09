from fastapi import FastAPI
# Thêm learning_request vào dòng import
from app.api.v1.endpoints import auth, coach_profile, learning_request

app = FastAPI(
    title="Swim360 API",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Swim360 API! The server is running correctly."}

# Gắn các router đã có
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(coach_profile.router, prefix="/api/v1/coach-profiles", tags=["Coach Profiles"])

# Gắn router mới cho "Yêu cầu học bơi"
app.include_router(learning_request.router, prefix="/api/v1/learning-requests", tags=["Learning Requests"])