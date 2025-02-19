from typing import Dict
from pydantic import BaseModel, Field


class Shift(BaseModel):
    start: str = Field(
        ...,
        title="Start",
        description="Start time",
        example="8:00",
    )
    end: str = Field(
        ...,
        title="End",
        description="End time",
        example="16:00",
    )


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
    shifts: Dict[str, Shift] = Field(
        ...,
    title="Shifs",
        description="Shifs",
        examples=[{"morning": "8:00-16:00"}, {"night": "20:00-4:00"}],
    )
