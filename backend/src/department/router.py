from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.utils import get_current_user
from src.database.factory import get_session
from src.database.nosql.json_db import JsonDatabase
from src.department.schemas import NewDepartment, UpdateDepartment
from src.department.models import Department
from typing import Annotated
from src.users.models import UserInDB

router = APIRouter(prefix="/departments", tags=["Departments"])
db_client = Annotated[JsonDatabase, Depends(get_session)]


@router.get("/{department_id}")
async def get_department(
    department_id: str,
    specialization_id: str,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    department = await database.get_department(department_id)
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    specialization = await database.get_specialization(specialization_id)
    if not specialization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user.specialization != specialization.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if department_id not in specialization.departments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return department


@router.post("/create")
async def create_department(
    department: NewDepartment,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    specialization = await database.get_specialization(user.specialization)
    if user.id not in specialization.admins:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if user.specialization != department.specialization:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    new_department = Department(**department.model_dump())
    await database.create_department(new_department)
    return new_department


@router.put("/{department_id}")
async def update_department(
    department_id: str,
    department: UpdateDepartment,
    database: db_client,
    user: Annotated[UserInDB, Depends(get_current_user)],
):
    specialization = await database.get_specialization(user.specialization)
    if user.id not in specialization.admins:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    department = await database.get_department(department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_department = Department(id=department_id, **department.model_dump())
    await database.update_department(updated_department)
    return updated_department
