from typing import Optional
from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: str
    email: str
    department: Optional[str] = Field(
        None,
        title="User department",
        description="User department",
        examples=["Engineering", "Marketing"],
    )


class UpdateRequest(BaseModel):
    user_id: str
    department: str = Field(
        None,
        title="Doctor department",
        description="Doctor department",
    )


class AssignRequest(BaseModel):
    user_mail: str
    specialization: str = Field(
        None,
        title="Doctor specialization",
        description="Doctor specialization",
    )
    department: str = Field(
        None,
        title="Doctor department",
        description="Doctor department",
    )
