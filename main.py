from fastapi import FastAPI, Depends
from schemas import StudentCreate, StudentUpdate, StudentResponse, UserCreate, UserLogin
from pymongo.collection import Collection
from bson import ObjectId
from auth import hash_password, verify_password, create_access_token, get_current_user
from dependencies import get_student_collection, get_user_collection
from fastapi.security import OAuth2PasswordRequestForm

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
    
    return {"msg" : "Student not found"}

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
    
    return {"msg" : "no updates"}

@app.patch("/students/{student_id}")
def patch_student(
    student_id: str,
    student: StudentUpdate,
    collection: Collection = Depends(get_student_collection)
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
    
    return {"msg" : "student not found"}

@app.post("/register")
def register(
    user: UserCreate,
    collection: Collection = Depends(get_user_collection)
):
    existing_user = collection.find_one({"username": user.username})

    if existing_user:
        return {"msg": "Username already exists"}

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
        return {"msg": "Invalid username or password"}

    if not verify_password(form_data.password, db_user["password"]):
        return {"msg": "Invalid username or password"}

    access_token = create_access_token(
    {"sub": form_data.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

