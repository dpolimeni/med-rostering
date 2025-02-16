from pydantic import BaseModel, Field

class Department(BaseModel):
    id: str
    name: str
    description: str
    type: str # low, medium, high
    users: list[str] = []
    