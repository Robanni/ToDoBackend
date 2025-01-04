
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from fastapi import HTTPException

from app.models.auth import User
from app.schemas.task import Task as Task_Schema
from app.models.task import Task

async def create_task(username: str, task: Task_Schema, db: AsyncSession):
    query = select(User).where(User.username == username)
    try:
        result = await db.execute(query)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")

    new_task = Task(title=task.title, description=task.description, completed=task.completed, user_id=existing_user.id)    

    db.add(new_task)
    try:
        await db.commit()
        await db.refresh(new_task)
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Failed to save user: {e}")
        raise HTTPException(status_code=500, detail="Failed to save Task")

    return {"msg": "Task successfully created", "task_id": new_task.id}
