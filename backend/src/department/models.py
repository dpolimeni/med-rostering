from pydantic import BaseModel, Field
from typing import List, Tuple
from uuid import uuid4


class Department(BaseModel):
    id: str = Field(
        default_factory=lambda x: str(uuid4()),
        title="ID",
        description="Department ID",
        example="ID_ginecology",
    )
    name: str
    description: str
    type: str  # low, medium, high
    users: List[str] = []
    constraints: List[Tuple[str, str]] = Field(
        [],
        title="Constraints",
        description="List of constraints",
        examples=[("monday", "shift-id"), ("tuesday", "shift-id")],
    )
