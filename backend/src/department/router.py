from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.utils import get_current_user
from src.database.factory import get_session
from src.database.nosql.json_db import JsonDatabase
from typing import Annotated
from src.users.models import UserInDB

router = APIRouter(prefix="/departments", tags=["Departments"])
db_client = Annotated[JsonDatabase, Depends(get_session)]

@router.get("/{department_id}")
async def get_department(
    department_id: str,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    department = await database.get_department(department_id)
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user.department != department.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return department