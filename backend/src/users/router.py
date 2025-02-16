from fastapi import APIRouter, Depends, HTTPException, status
from src.users.models import UserInDB
from src.database.nosql.json_db import JsonDatabase
from src.database.factory import get_session
from src.settings import app_settings
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])
db_client = Annotated[JsonDatabase, Depends(get_session)]



