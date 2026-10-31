from app.crud.base import CRUDBase
from app.models.Users import Users
from app.schemas.users import UsersCreate,UsersUpdate
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.db.session import get_session
from typing import Awaitable
from app.core import auth


class USERSCrud(CRUDBase[Users,UsersCreate,UsersUpdate]):
    def create_user(self,users:UsersCreate,db:AsyncSession|Session=Depends(get_session))->Users|Awaitable[Users]:
        if isinstance(db,AsyncSession):
            return self.create_user_async(users,db)
        datas=users.model_dump()
        datas["hashed_password"]=auth.hash_password(datas["password"])
        del datas["password"]
        return self.create(db,datas)

    async def create_user_async(self,users:UsersCreate,db:AsyncSession=Depends(get_session))->Users:
        datas=users.model_dump()
        datas["hashed_password"]=auth.hash_password(datas["password"])
        del datas["password"]
        return await self.create_async(db,datas)


users=USERSCrud(Users)