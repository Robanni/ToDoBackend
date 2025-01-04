from app.models.auth import User
from app.utils.database import get_db
from app.schemas.auth import UserRegistration, UserBase
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.jwt_conf import  auth

from app.services.auth import register_user, login_user
from app.services.task import create_task
from app.schemas.task import Task

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


@router.post("/create_task")
async def protected_route(task: Task, current_user: User =  Depends(auth.get_current_subject), db: AsyncSession = Depends(get_db)):
    user = await current_user
    return await create_task(user.username, task, db)
