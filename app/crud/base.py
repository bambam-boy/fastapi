from typing import TypeVar,Generic,Awaitable,Any,Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.db.baseclass import Base
from pydantic import BaseModel
from asyncio import iscoroutine
from sqlalchemy import select
from datetime import datetime


ModelType=TypeVar("ModelType",bound=Base)
ModelCreateType=TypeVar("ModelCreateType",bound=BaseModel)
ModelUpdateType=TypeVar("ModelUpdateType",bound=BaseModel)


class CRUDBase(Generic[ModelType,ModelCreateType,ModelUpdateType]):
    def __init__(self,model:ModelType):
        self.model=model


    def commit_and_refresh(self,db_obj:ModelType,db:Session|AsyncSession)->ModelType|Awaitable[ModelType]:
        if isinstance(db,AsyncSession):
            return self.commit_and_refresh_async(db_obj,db)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    async def commit_and_refresh_async(self,db_obj:ModelType,db:AsyncSession)->ModelType:
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


    def get_first(self,scalars)->ModelType|Awaitable[ModelType]|None:
        if iscoroutine(scalars):
            return self.get_first_async(scalars)
        return scalars.first()
        

    async def get_first_async(self,scalars)->ModelType|None:
        value= await scalars
        return value.first()


    def get_last(self,scalars)->ModelType|Awaitable[ModelType]|None:
        if iscoroutine(scalars):
            return self.get_last_async(scalars)
        return scalars.last()


    async def get_last_async(self,scalars)->ModelType|None:
        value=await scalars
        return value.last()


    def get_all(self,scalars)->list[ModelType]|Awaitable[list[ModelType]]:
        if iscoroutine(scalars):
            return self.get_all_async(scalars)
        return scalars.all()


    async def get_all_async(self,scalars)->list[ModelType]:
        values=await scalars
        return values.all()


    def get_multi(
        self,
        db:Session|AsyncSession,
        skip:int=0,
        limit:int=100,
        asc:bool=False)->list[ModelType]|Awaitable[list[ModelType]]:

        if isinstance(db,AsyncSession):
            return self.get_multi_async(db,skip,limit,asc)
        
        query=(
            select(self.model).
            order_by(self.model.id.asc() if asc else self.model.id.desc()).
            offset(skip)
        )
        
        if not limit is None or not limit == 0:
            return self.get_all(db.scalars(query))
        
        return self.get_all(db.scalars(query.limit(limit)))


    async def get_multi_async(        
        self,
        db:Session|AsyncSession,
        skip:int=0,
        limit:int=100,
        asc:bool=False)->list[ModelType]:

        query=(
            select(self.model).
            order_by(self.model.id.asc() if asc else self.model.id.desc()).
            offset(skip)
        )

        if not limit is None or not limit == 0:
            return await self.get_all_async(db.scalars(query))
        
        return await self.get_all_async(db.scalars(query.limit(limit)))


    def get_by_id(self,id:Any,db:Session|AsyncSession)->ModelType|Awaitable[ModelType]:
        if isinstance(db,AsyncSession):
            return self.get_by_id_async(id,db)
        value=select(self.model).where(self.model.id==id)
        return self.get_first(db.scalars(value))


    async def get_by_id_async(self,id:Any,db:AsyncSession)->ModelType:
        value=select(self.model).where(self.model.id==id)
        return await self.get_first_async(db.scalars(value))


    def create(self,db:Session|AsyncSession,values:ModelCreateType)->ModelType|Awaitable[ModelType]:
        if isinstance(db,AsyncSession):
            return self.create_async(db,values)
        if not isinstance(values,Dict):
            values=values.model_dump(exclude_unset=True)
        db_obj=self.model(**values)
        db.add(db_obj)
        return self.commit_and_refresh(db_obj,db)

        
    async def create_async(self,db:AsyncSession,values:ModelCreateType|Dict[str,Any])->ModelType:
        if not isinstance(values,Dict):
            values=values.model_dump(exclude_unset=True)
        db_obj=self.model(**values)
        db.add(db_obj)
        return await self.commit_and_refresh_async(db_obj,db)


    def update(self,db:Session|AsyncSession,db_obj:ModelType,values:ModelUpdateType)->ModelType|Awaitable[ModelType]:
        if isinstance(db,AsyncSession):
            return self.update_async(db,db_obj,values)
        datas=values.model_dump(exclude_unset=True)
        for item in datas:
            setattr(db_obj,item,datas[item])
        setattr(db_obj,"mod_at",datetime.utcnow())
        return self.commit_and_refresh(db_obj,db)


    async def update_async(self,db:AsyncSession,db_obj:ModelType,values:ModelUpdateType)->ModelType:
        datas=values.model_dump(exclude_unset=True)
        for item in datas:
            setattr(db_obj,item,datas[item])
        setattr(db_obj,"mod_at",datetime.utcnow())
        return await self.commit_and_refresh_async(db_obj,db)


    def remove(self,db:Session|AsyncSession,id:Any)->ModelType|Awaitable[ModelType]:
        if isinstance(db,AsyncSession):
            return self.remove_async(db,id)
        db_obj=self.get_by_id(id,db)
        setattr(db_obj,"mod_at",datetime.utcnow())
        setattr(db_obj,"is_deleted",True)
        return self.commit_and_refresh(db_obj,db)


    async def remove_async(self,db:AsyncSession,id:Any)->ModelType:
        db_obj=await self.get_by_id(id,db)
        setattr(db_obj,"mod_at",datetime.utcnow())
        setattr(db_obj,"is_deleted",True)
        return await self.commit_and_refresh_async(db_obj,db)