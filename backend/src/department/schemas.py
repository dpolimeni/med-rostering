from pydantic import BaseModel, Field
from typing import List, Tuple

class NewDepartment(BaseModel):
    name: str
    description: str
    type: str  = Field(
        ...,
        title="Type",
        description="Department type (low, medium, high)",
        example="low",
    )
    users: List[str] = []
    constraints: List[Tuple[str, str]] = Field(
        [],
        title="Constraints",
        description="List of constraints",
        examples=[("monday", "shift-id"), ("tuesday", "shift-id")],
    )
    specialization: str = Field(
        None,
        title="Specialization",
        description="Specialization id",
        example="ID_ginecology",
    )
