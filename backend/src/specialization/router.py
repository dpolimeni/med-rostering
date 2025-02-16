from fastapi import APIRouter, Depends, HTTPException, status
from src.users.models import UserInDB
from src.specialization.models import Specialization
from src.database.factory import get_session
from typing import Annotated
from src.database.nosql.json_db import JsonDatabase
from src.auth.utils import get_current_user


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

    if user.department not in specialization.departments:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return specialization
