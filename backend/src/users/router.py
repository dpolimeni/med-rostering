from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.utils import get_current_user
from src.database.factory import get_session
from src.database.nosql.json_db import JsonDatabase
from src.users.models import UserInDB
from src.users.schemas import AssignRequest, UpdateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])
db_client = Annotated[JsonDatabase, Depends(get_session)]


@router.get("/me")
async def read_user(database: db_client, user: UserInDB = Depends(get_current_user)):
    return UserResponse(
        id=user.id,
        email=user.email,
        department=user.department,
        specialization=user.specialization,
    )


@router.put("/update")
async def update_user(
    new_department: UpdateRequest,
    database: db_client,
    user: UserInDB = Depends(get_current_user),
):
    # If is another user trying to update the department check users are in the same specialization and the user is an admin
    if new_department.user_id != user.id:
        if "admin" not in user.roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        to_update_user = await database.get_user(new_department.user_id)
        if to_update_user.specialization != user.specialization:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Users are not in the same specialization",
            )
    else:
        to_update_user = user
    to_update_user.department = new_department.department
    await database.update_user(to_update_user)
    return UserResponse(
        email=user.email, department=user.department, specialization=user.specialization
    )


@router.patch("/assign")
async def assign_specialization(
    assign_request: AssignRequest,
    database: db_client,
    user: UserInDB = Depends(get_current_user),
):
    if "admin" not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    to_assign_user = await database.get_user(assign_request.user_mail)
    if not to_assign_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    to_assign_user.specialization = assign_request.specialization
    to_assign_user.department = assign_request.department
    await database.update_user(to_assign_user)
    return {"message": "User assigned"}

# TODO
# @router.delete("/delete")
# @router.get("/list")
