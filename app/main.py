from fastapi import FastAPI
# SỬA LỖI: Thêm `payment` vào dòng import này
from app.api.v1.endpoints import auth, coach_profile, learning_request, course, offer, payment

app = FastAPI(
    title="Swim360 API",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Swim360 API! The server is running correctly."}

# Gắn các router
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(coach_profile.router, prefix="/api/v1/coach-profiles", tags=["Coach Profiles"])
app.include_router(learning_request.router, prefix="/api/v1/learning-requests", tags=["Learning Requests"])
app.include_router(course.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(offer.router, prefix="/api/v1", tags=["Offers"])
app.include_router(payment.router, prefix="/api/v1/payments", tags=["Payments"])