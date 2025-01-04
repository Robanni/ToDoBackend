import os
from dotenv import load_dotenv
from authx import AuthX, AuthXConfig
from fastapi import Depends, HTTPException
from requests import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.auth import User
from app.utils.database import get_db_context

load_dotenv()

jwt_config = AuthXConfig(
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    JWT_ALGORITHM="HS256",
)
auth = AuthX(jwt_config)


@auth.set_subject_getter
async def get_user(uid: str) -> User:
    async with get_db_context() as db:
        query = select(User).where(User.id == int(uid))
        result = await db.execute(query)
        user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
