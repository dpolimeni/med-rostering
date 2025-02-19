from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.utils import get_current_user
from src.database.factory import get_session
from src.database.nosql.json_db import JsonDatabase
from src.specialization.models import Specialization
from src.specialization.schemas import NewSpecialization
from src.users.models import UserInDB
from src.users.schemas import UserResponse

router = APIRouter(prefix="/specializations", tags=["Specializations"])
db_client = Annotated[JsonDatabase, Depends(get_session)]


@router.get("/{specialization_id}", response_model=Specialization)
async def get_specialization(
    specialization_id: str,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    specialization = await database.get_specialization(specialization_id)
    if not specialization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user.specialization not in specialization.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return specialization


@router.post("/create", response_model=Specialization)
async def create_specialization(
    specialization: NewSpecialization,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    new_specialization = Specialization(admins=[user.id], **specialization.model_dump())
    await database.create_specialization(new_specialization, user)
    return specialization


@router.get("/{specialization_id}/users")
async def get_specialization_users(
    specialization_id: str,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    specialization = await database.get_specialization(specialization_id)
    if not specialization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user.specialization != specialization.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    specialization_users = []
    users_client = database.user_client
    for db_user in users_client:
        if db_user["specialization"] == specialization.id:
            specialization_users.append(UserResponse(**db_user))

    return specialization_users


@router.post("/{specialization_id}/user/{user_email}")
async def assign_specialization(
    specialization_id: str,
    user_email: str,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    specialization = await database.get_specialization(specialization_id)
    if user.id not in specialization.admins:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    assign_user = await database.get_user(user_email)
    if not assign_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    ## TODO INVITATION FLOW
    assign_user.specialization = specialization_id
    await database.update_user(assign_user)

    return {"message": "User assigned to specialization"}
