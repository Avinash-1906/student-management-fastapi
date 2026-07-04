from pydantic import BaseModel, Field
from typing import Literal


class StudentCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Student name"
    )

    age: int = Field(
        ge=16,
        le=60,
        description="Age must be between 16 and 60"
    )

    department: str = Field(
        min_length=2,
        max_length=30,
        description="Department name"
    )


class StudentUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    age: int | None = Field(
        default=None,
        ge=16,
        le=60
    )

    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=30
    )


class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    department: str


class UserCreate(BaseModel):
    username: str
    password: str
    role: Literal["admin", "user"]


class UserLogin(BaseModel):
    username: str
    password: str