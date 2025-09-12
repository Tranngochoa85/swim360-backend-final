from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.api.v1.dependencies import get_current_user, get_coach_profile_id
from app.api.v1.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from supabase import Client
from app.core.supabase_client import supabase
from typing import List
import json
from datetime import date, datetime
from uuid import UUID

def json_converter(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, UUID):
        return str(o)

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Client = Depends(lambda: supabase),
    coach_id: str = Depends(get_coach_profile_id)
):
    course_dict = course_data.model_dump()
    course_dict['coach_id'] = str(coach_id)
    try:
        inserted_data = db.table("courses").insert(course_dict).execute()
        json_string = json.dumps(inserted_data.data[0], default=json_converter)
        return Response(content=json_string, media_type="application/json", status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-courses")
def get_my_courses(
    db: Client = Depends(lambda: supabase),
    coach_id: str = Depends(get_coach_profile_id)
):
    courses_res = db.table("courses").select("*").eq("coach_id", coach_id).execute()
    json_string = json.dumps(courses_res.data, default=json_converter)
    return Response(content=json_string, media_type="application/json")

@router.put("/{course_id}")
def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    db: Client = Depends(lambda: supabase),
    coach_id: str = Depends(get_coach_profile_id)
):
    course_to_update = db.table("courses").select("id").eq("id", str(course_id)).eq("coach_id", coach_id).single().execute()
    if not course_to_update.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học hoặc bạn không có quyền chỉnh sửa.")
    
    update_dict = course_data.model_dump(exclude_unset=True)
    
    # SỬA LỖI: Bỏ .select().single() không hợp lệ khỏi chuỗi lệnh update
    updated_res = db.table("courses").update(update_dict).eq("id", str(course_id)).execute()
    
    if not updated_res.data:
        raise HTTPException(status_code=500, detail="Cập nhật khóa học thất bại.")

    json_string = json.dumps(updated_res.data[0], default=json_converter)
    return Response(content=json_string, media_type="application/json")

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: UUID,
    db: Client = Depends(lambda: supabase),
    coach_id: str = Depends(get_coach_profile_id)
):
    course_to_delete = db.table("courses").select("id").eq("id", str(course_id)).eq("coach_id", coach_id).single().execute()
    if not course_to_delete.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học hoặc bạn không có quyền xóa.")
        
    db.table("courses").delete().eq("id", str(course_id)).execute()
    return Response(status_code=status.HTTP_204_NO_CONTENT)