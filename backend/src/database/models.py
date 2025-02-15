from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class User(BaseModel):
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


class DriveIntegration(BaseModel):
    access_token: str
    refresh_token: str


class UserInDB(User):
    hashed_password: Optional[str] = Field(
        None,
        title="Hashed password",
        description="Hashed password",
        examples=["$2b$12$zWfz2iN7vLX5w1yH7b1y9e"],
    )
    integrations: Dict[str, DriveIntegration] = Field(
        {},
        title="User integrations",
        description="User integrations",
        examples=[
            {"google_drive": {"access_token": "token", "refresh_token": "token"}}
        ],
    )
