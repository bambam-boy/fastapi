import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from pwdlib import PasswordHash
from app.core.config import settings
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException,status
from app.models.Users import Users
from sqlalchemy import select



password_hash=PasswordHash.recommended()
auth_token=OAuth2PasswordBearer(tokenUrl="api/users/token")

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hash.verify(plain_password,hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.exp_token_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(), 
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token:str)->str|None:
    try:
        pyload=jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=settings.ALGORITHM,
            options={"require":["sub"]}
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return pyload.get("sub")



async def get_current_user(token:str,db:AsyncSession=Depends(get_session))->Users:
    user_model=verify_access_token(token)
    if user_model in None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id_int=int(user_model)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    q=await db.execute(select(Users).where(Users.id==user_id_int))
    user=q.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user



    
