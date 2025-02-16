from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Dict, List


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
    low_workload_departments: List[str] = []
    shifs: Dict[str, str] = Field(
        ...,
        title="Shifs",
        description="Shifs",
        examples=[{"morning": "8:00-16:00"}, {"night": "20:00-4:00"}],
    )
