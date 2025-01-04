import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from fastapi import HTTPException

from app.models.auth import User
from app.utils.jwt_conf import auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(email: str, username: str, password: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    try:
        result = await db.execute(query)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error  {e}")
    
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(password)


    new_user = User(email=email, username=username, hashed_password=hashed_password)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save user")

    return {"msg": "User successfully registered", "user_id": new_user.id}


async def login_user(email: str, password: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    try:
        result = await db.execute(query)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    existing_user = result.scalars().first()

    if not existing_user or not pwd_context.verify(password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = auth.create_access_token(subject=email, uid=str(existing_user.id))

    return {"access_token": access_token, "token_type": "bearer"}

