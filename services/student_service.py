from bson import ObjectId
from fastapi import HTTPException
from repositories.student_repository import create_student, get_all_students, get_student, update_student, delete_student
from schemas import StudentResponse
from logger import logger

def create_student(student, collection):

    student_dict = student.model_dump()

    result = create_student(
        student_dict,
        collection
    )

    logger.info(
        f"Student created with id {result.inserted_id}"
    )

    return {
        "msg": "Student created.",
        "id": str(result.inserted_id)
    }


def get_all_students(query, skip, limit, collection):

    students = get_all_students(
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

    return response


def get_student(student_id, collection):

    student = collection.find_one(
        {"_id": ObjectId(student_id)}
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

    result = update_student(
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

    return {
        "msg": "Student updated successfully"
    }


def patch_student(student_id, student, collection):

    student_dict = student.model_dump(exclude_unset=True)

    result = update_student(
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

    return {
        "msg": "Student updated successfully"
    }


def delete_student(student_id, collection):

    result = delete_student(
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

    return {
        "msg": "Student deleted successfully"
    }