from fastapi.routing import APIRouter
from fastapi import Depends
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select,func
from app.core.config import settings
from app.schemas.users import UsersCreate,UsersUpdate,UsersResponcePublic,UsersResponcePrivete
from app.schemas.token import Token 
from app import crud
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import (
    auth_token,
    create_access_token,
    hash_password,
    verify_access_token,
    verify_password,
    get_current_user
)




router=APIRouter()


@router.post("/create_account")
async def create_user(users:UsersCreate,db:AsyncSession=Depends(get_session)):
    return await crud.users.create_user_async(users,db)


@router.get("/me")
async def get_current_user(db:AsyncSession=Depends(get_session)):
    return await get_current_user(db)
