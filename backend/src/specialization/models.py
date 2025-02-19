from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Dict, List
from .schemas import Shift


class Specialization(BaseModel):
    id: str = Field(
        default_factory=lambda x: str(uuid4()),
        title="ID",
        description="Specialization ID",
        example="ID_ginecology",
    )
    name: str
    description: str
    departments: List[str] = Field(
        [],
        title="Departments",
        description="List of Departments id",
        examples=["ID_ginecology", "ID_surgery"],
    )
    admins: List[str] = Field(
        [],
        title="Admins",
        description="List of Owners id",
        examples=["ID_admin1", "ID_admin2"],
    )
    low_workload_departments: List[str] = []
    shifts: Dict[str, Shift] = Field(
        ...,
        title="Shifs",
        description="Shifs",
        examples=[{"morning": {"start": "8:00", "end": "16:00"}}],
    )
