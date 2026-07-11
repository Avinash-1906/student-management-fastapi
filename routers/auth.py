from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.collection import Collection

from dependencies import get_user_collection
from schemas import UserCreate
from services.auth_service import register, login


auth_router = APIRouter(
    tags=["Authentication"]
)


@auth_router.post("/register")
def register_user(
    user: UserCreate,
    collection: Collection = Depends(get_user_collection)
):

    return register(
        user,
        collection
    )


@auth_router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    collection: Collection = Depends(get_user_collection)
):

    return login(
        form_data,
        collection
    )


