from typing import List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class UserInDB(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        title="User ID",
        description="User ID",
        examples=["f8a3c4c6-3d7b-4e6b-9b7b-5c6c8d1a2b9a"],
    )
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
    specialization: Optional[str] = Field(
        None,
        title="Specialization",
        description="Doctor specialization",
        examples=["ID_Ginecology_1st_year", "ID_Cardiology_2nd_year"],
    )
    department: Optional[str] = Field(
        None,
        title="Department",
        description="Doctor department",
        examples=["ID_ginecology", "ID_surgery"],
    )
