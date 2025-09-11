from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.api.v1.dependencies import get_current_user
from app.api.v1.schemas.course import CourseCreate, CourseResponse
from supabase import Client
from app.core.supabase_client import supabase
from typing import List
import json
from datetime import date, datetime
from uuid import UUID

# --- DẤU HIỆU NHẬN BIẾT ---
print(">>> ĐANG CHẠY PHIÊN BẢN COURSE.PY CUỐI CÙNG - GIẢI PHÁP TỐI THƯỢỢNG <<<")
# -------------------------

# --- BỘ CHUYỂN ĐỔI JSON TÙY CHỈNH (ĐÃ NÂNG CẤP) ---
def json_converter(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, UUID):
        return str(o)
# ----------------------------------------------------

router = APIRouter()

def get_coach_profile_id(user_id: str, db: Client) -> str:
    profile_res = db.table("coach_profiles").select("id").eq("user_id", user_id).eq("status", "approved").single().execute()
    if not profile_res.data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Người dùng không phải là HLV đã được duyệt.")
    return profile_res.data['id']


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    coach_id = get_coach_profile_id(current_user.id, db)
    course_dict = course_data.model_dump()
    course_dict['coach_id'] = str(coach_id)

    try:
        inserted_data = db.table("courses").insert(course_dict).execute()
        if not inserted_data.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Không thể tạo khóa học.")
        
        raw_data = inserted_data.data[0]
        json_string = json.dumps(raw_data, default=json_converter)
        return Response(content=json_string, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/my-courses")
def get_my_courses(
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    coach_id = get_coach_profile_id(current_user.id, db)
    courses_res = db.table("courses").select("*").eq("coach_id", coach_id).execute()
    
    json_string = json.dumps(courses_res.data, default=json_converter)
    return Response(content=json_string, media_type="application/json")