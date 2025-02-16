from typing import Optional
from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    email: str
    department: Optional[str] = Field(
        None,
        title="User department",
        description="User department",
        examples=["Engineering", "Marketing"],
    )
