from fastapi import HTTPException, status
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from repositories import user_repository
from logger import logger


def register(user, collection):

    existing_user = user_repository.get_user_by_username(
        user.username,
        collection
    )

    if existing_user:

        logger.error(
            f"Registration failed. Username '{user.username}' already exists."
        )

        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    user_dict = user.model_dump()

    user_dict["password"] = hash_password(user.password)

    result = user_repository.create_user(
        user_dict,
        collection
    )

    logger.info(
        f"User '{user.username}' registered successfully"
    )

    return {
        "msg": "User registered successfully",
        "id": str(result.inserted_id)
    }


def login(form_data, collection):

    db_user = user_repository.get_user_by_username(
        form_data.username,
        collection
    )

    if db_user is None:

        logger.error(
            f"Login failed for username '{form_data.username}'"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        db_user["password"]
    ):

        logger.error(
            f"Invalid password for '{form_data.username}'"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {
            "sub": form_data.username,
            "role": db_user["role"]
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": form_data.username,
            "role": db_user["role"]
        }
    )

    logger.info(
        f"User '{form_data.username}' logged in successfully"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }