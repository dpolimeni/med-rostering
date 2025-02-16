from fastapi import APIRouter, Depends, HTTPException, status
from src.users.models import UserInDB
from src.database.nosql.json_db import JsonDatabase
from src.database.factory import get_session
from src.settings import app_settings
from typing import Annotated
from src.auth.utils import get_current_user
from src.users.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])
db_client = Annotated[JsonDatabase, Depends(get_session)]


@router.get("/me")
async def read_user(database: db_client, user: UserInDB = Depends(get_current_user)):
    return UserResponse(email=user.email, register_status=user.register_status)


