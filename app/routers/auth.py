from app.models.auth import User
from app.services.auth import register_user, login_user
from app.utils.database import get_db
from app.schemas.auth import UserRegistration, UserBase
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.jwt_conf import  auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register_user_endpoint(register: UserRegistration, db: AsyncSession = Depends(get_db)):
    try:
        return await register_user(register.email, register.username, register.password, db)
    except HTTPException as e:
        raise e


@router.post("/login")
async def login_user_endpoint(login: UserBase, db: AsyncSession = Depends(get_db)):
    try:
        return await login_user(login.email, login.password, db)
    except HTTPException as e:
        raise e


@router.get("/protected")
async def protected_route(current_user: User =  Depends(auth.get_current_subject)):
    user = await current_user
    return {"msg": f"Hello, {user.email}"}
