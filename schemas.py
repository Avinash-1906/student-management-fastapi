from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    department: str


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    department: str | None = None


class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    department: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str