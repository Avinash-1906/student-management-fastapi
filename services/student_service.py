from bson import ObjectId
from fastapi import HTTPException 
from repositories import student_repository
from schemas import StudentResponse
from logger import logger
import os
import shutil
import uuid
import json
from cache import redis_client


def create_student(
    student,
    idempotency_key,
    student_collection,
    idempotency_collection
):

    existing = idempotency_collection.find_one(
        {
            "_id": idempotency_key
        }
    )

    if existing:
        return existing["response"]

    student_dict = student.model_dump()

    result = student_repository.create_student(
        student_dict,
        student_collection
    )

    for key in redis_client.scan_iter("students*"):
        redis_client.delete(key)

    response = {
        "msg": "Student created.",
        "id": str(result.inserted_id)
    }

    idempotency_collection.insert_one(
        {
            "_id": idempotency_key,
            "response": response
        }
    )

    logger.info(
        f"Student created with id {result.inserted_id}"
    )

    return response


def get_all_students(query, skip, limit, collection):

    cache_key = f"students:{query}:{skip}:{limit}"

    cached_data = redis_client.get(cache_key)

    if cached_data:
        print("Cache HIT")
        return [
            StudentResponse(**student)
            for student in json.loads(cached_data)
        ]

    print("Cache MISS")

    students = student_repository.get_all_students(
        query,
        skip,
        limit,
        collection
    )

    response = []

    for student in students:
        response.append(
            StudentResponse(
                id=str(student["_id"]),
                name=student["name"],
                age=student["age"],
                department=student["department"]
            )
        )

    redis_client.set(
        cache_key,
        json.dumps(
            [student.model_dump() for student in response]
        ),
        ex=60
    )

    print("Cache Key:", cache_key)
    print("Stored:", redis_client.get(cache_key))
    print("Keys:", list(redis_client.scan_iter("*")))

    return response


def get_student(student_id, collection):

    student = student_repository.get_student(
        student_id,
        collection
    )

    if student is None:
        logger.error(
            f"Student {student_id} not found"
        )

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student["_id"] = str(student["_id"])

    return student


def update_student(student_id, student, collection):

    student_dict = student.model_dump(exclude_unset=True)

    result = student_repository.update_student(
        student_id,
        student_dict,
        collection
    )

    if result.matched_count == 0:

        logger.error(
            f"Student {student_id} not found"
        )

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if result.modified_count == 0:

        logger.info(
            f"No changes made for student {student_id}"
        )

        raise HTTPException(
            status_code=400,
            detail="No changes made"
        )

    logger.info(
        f"Student {student_id} updated successfully"
    )

    for key in redis_client.scan_iter("students*"):
        redis_client.delete(key)

    return {
        "msg": "Student updated successfully"
    }


def patch_student(student_id, student, collection):

    student_dict = student.model_dump(exclude_unset=True)

    result = student_repository.update_student(
        student_id,
        student_dict,
        collection
    )

    if result.matched_count == 0:

        logger.error(
            f"Student {student_id} not found"
        )

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if result.modified_count == 0:

        logger.info(
            f"No changes made for student {student_id}"
        )

        raise HTTPException(
            status_code=400,
            detail="No changes made"
        )

    logger.info(
        f"Student {student_id} patched successfully"
    )

    for key in redis_client.scan_iter("students*"):
        redis_client.delete(key)

    return {
        "msg": "Student updated successfully"
    }


def delete_student(student_id, collection):

    result = student_repository.delete_student(
        student_id,
        collection
    )

    if result.deleted_count == 0:

        logger.error(
            f"Student {student_id} not found"
        )

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    logger.info(
        f"Student {student_id} deleted successfully"
    )

    for key in redis_client.scan_iter("students*"):
        redis_client.delete(key)

    return {
        "msg": "Student deleted successfully"
    }



def upload_student_file(file):

    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    upload_path = os.path.join(
        "uploads",
        unique_filename
    )

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "File uploaded successfully",
        "filename": unique_filename
    }