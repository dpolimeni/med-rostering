from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class UserInDB(BaseModel):
    email: str
    roles: List[str] = Field(
        ["user"],
        title="User roles",
        description="User roles",
        examples=[["admin"], ["user"], ["editor"]],
    )
    register_status: Optional[str] = Field(
        "pending",
        title="User registration status",
        description="User registration status",
        examples=["pending", "active"],
    )
    hashed_password: Optional[str] = Field(
        None,
        title="Hashed password",
        description="Hashed password",
        examples=["$2b$12$zWfz2iN7vLX5w1yH7b1y9e"],
    )
    department: Optional[str] = Field(
        None,
        title="User department",
        description="User department",
        examples=["Engineering", "Marketing"],
    )
    