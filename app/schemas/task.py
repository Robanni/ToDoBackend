from pydantic import BaseModel, EmailStr


class Task(BaseModel):
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True  # Чтобы Pydantic мог работать с SQLAlchemy моделями