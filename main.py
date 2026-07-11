from fastapi import FastAPI

from routers.student import student_router
from routers.auth import auth_router
from routers.websocket import websocket_router

app = FastAPI()

app.include_router(student_router)
app.include_router(auth_router)
app.include_router(websocket_router)

''' 

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from schemas import StudentCreate, StudentUpdate, StudentResponse, UserCreate, UserLogin
from pymongo.collection import Collection
from bson import ObjectId
from auth import hash_password, verify_password, create_access_token, create_refresh_token,  get_current_user
from dependencies import get_student_collection, get_user_collection
from fastapi.security import OAuth2PasswordRequestForm
import shutil
import os
import uuid

app = FastAPI()

@app.post("/students")
def create_student(
    student: StudentCreate,
    collection: Collection = Depends(get_student_collection),
    current_user=Depends(get_current_user)
):
    student_dict = student.model_dump()

    result = collection.insert_one(student_dict)

    return{
        "msg" : "Student created.",
        "id" : str(result.inserted_id)
    }

@app.get("/students", response_model=list[StudentResponse])
def find_all_students(
    collection: Collection = Depends(get_student_collection),
    current_user=Depends(get_current_user)
):
    students = []

    for student in collection.find():
        students.append(
            StudentResponse(
                id=str(student["_id"]),
                name=student["name"],
                age=student["age"],
                department=student["department"]
            )
        )

    return students

@app.get("/students/{student_id}")
def get_student(
    student_id : str,
    collection: Collection = Depends(get_student_collection),
    current_user=Depends(get_current_user)
):
    student = collection.find_one({"_id" : ObjectId(student_id)})

    if student:
        student["_id"] = str(student["_id"])
        return student
    
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.put("/students/{student_id}")
def update_student(
    student_id : str,
    student : StudentUpdate,
    collection: Collection = Depends(get_student_collection),
    current_user=Depends(get_current_user)
):
    student_dict = student.model_dump(exclude_unset=True)

    result = collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set" : student_dict}
    )

    if result.modified_count == 1:
        return {"msg" : "student have been updated"}
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="No changes made"
        )

    return {"msg": "Student updated successfully"}

@app.patch("/students/{student_id}")
def patch_student(
    student_id: str,
    student: StudentUpdate,
    collection: Collection = Depends(get_student_collection),
    current_user=Depends(get_current_user)
):
    student_dict = student.model_dump(exclude_unset=True)

    result = collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": student_dict}
    )

    if result.matched_count == 0:
        return {"msg": "Student not found"}

    if result.modified_count == 0:
        return {"msg": "No changes made"}

    return {"msg": "Student updated successfully"}

@app.delete("/students/{student_id}")
def delete_student(
    student_id : str,
    collection: Collection = Depends(get_student_collection),
    current_user=Depends(get_current_user)
):

    result = collection.delete_one(
        {"_id" : ObjectId(student_id)}  
    )

    if result.deleted_count == 1:
        return {"msg" : "student have been deleted"}
    
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.post("/register")
def register(
    user: UserCreate,
    collection: Collection = Depends(get_user_collection)
):
    existing_user = collection.find_one({"username": user.username})

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)

    result = collection.insert_one(user_dict)

    return {
        "msg": "User registered successfully",
        "id": str(result.inserted_id)
    }

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    collection: Collection = Depends(get_user_collection)
):
    db_user = collection.find_one({"username": form_data.username})

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {"sub": form_data.username}
    )

    refresh_token = create_refresh_token(
        {"sub": form_data.username}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/students/upload")
def upload_file(file: UploadFile = File(...)):

    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    upload_path = os.path.join("uploads", unique_filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": unique_filename
    }

@app.post("/refresh")
def refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        new_access_token = create_access_token(
            {"sub": username}
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
        
'''