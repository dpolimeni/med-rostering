from typing import Dict
from pydantic import BaseModel, Field


class NewSpecialization(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="Specialization name",
        example="Ginecology",
    )
    description: str = Field(
        ...,
        title="Description",
        description="Specialization description",
        example="Ginecology is the medical practice dealing with the health",
    )
    shifs: Dict[str, str] = Field(
        ...,
        title="Shifs",
        description="Shifs",
        examples=[{"morning": "8:00-16:00"}, {"night": "20:00-4:00"}],
    )
