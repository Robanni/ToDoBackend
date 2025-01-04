from pydantic import BaseModel, EmailStr


class Task(BaseModel):
    title: str
    description: str
    completed: bool

