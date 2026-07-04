from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson import ObjectId
from services.student_service import create_student, get_all_students, get_student, update_student, patch_student, delete_student

from auth import get_current_admin
from schemas import StudentCreate, StudentUpdate, StudentResponse
from dependencies import get_student_collection

student_router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@student_router.post("")
def add_student(
    student: StudentCreate,
    collection: Collection = Depends(get_student_collection)
):

    return create_student(
        student,
        collection
    )

@student_router.get("", response_model=list[StudentResponse])
def find_all_students(
    page: int = 1,
    limit: int = 10,
    department: str | None = None,
    name: str | None = None,
    collection: Collection = Depends(get_student_collection)
):
    
    skip = (page - 1) * limit

    query = {}

    if department:
        query["department"] = department

    if name:
        query["name"] = {
            "$regex": name,
            "$options": "i"
        }

    return get_all_students(
        query,
        skip,
        limit,
        collection
    )


@student_router.get("/{student_id}")
def find_student(
    student_id: str,
    collection: Collection = Depends(get_student_collection)
):
    return get_student(
        student_id,
        collection
    )


@student_router.put("/{student_id}")
def update_student_route(
    student_id: str,
    student: StudentUpdate,
    collection: Collection = Depends(get_student_collection)
):

    return update_student(
        student_id,
        student,
        collection
    )


@student_router.patch("/{student_id}")
def patch_student_route(
    student_id: str,
    student: StudentUpdate,
    collection: Collection = Depends(get_student_collection)
):

    return patch_student(
        student_id,
        student,
        collection
    )


@student_router.delete("/{student_id}")
def delete_student_route(
    student_id: str,
    current_user=Depends(get_current_admin),
    collection: Collection = Depends(get_student_collection)
):

    return delete_student(
        student_id,
        collection
    )