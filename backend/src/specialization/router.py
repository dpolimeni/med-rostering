from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.utils import get_current_user
from src.database.factory import get_session
from src.database.nosql.json_db import JsonDatabase
from src.specialization.models import Specialization
from src.specialization.schemas import NewSpecialization
from src.users.models import UserInDB

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
    # if "admin" not in user.roles:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    specialization = Specialization(**specialization.model_dump())
    await database.create_specialization(specialization, user)
    return specialization
