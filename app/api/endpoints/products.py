from fastapi.routing import APIRouter
from app import crud
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.products import ProductsCreate,ProductsUpdate


router=APIRouter()


@router.get("/get/multi")
async def get_multi_products(db:AsyncSession=Depends(get_session),skip:int=0,limit:int=100,asc:bool=False):
    return await crud.products.get_multi_async(db,skip,limit,asc)


@router.get("/get/id")
async def get_product_by_id(id:str,db:AsyncSession=Depends(get_session)):
    return await crud.products.get_by_id_async(id,db)


@router.post("/add/single")
async def insert_single_product(value:ProductsCreate,db:AsyncSession=Depends(get_session)):
    return await crud.products.create_async(db,value)


@router.post("/add/multi")
async def insert_multi_products(values:list[ProductsCreate],db:AsyncSession=Depends(get_session)):
    datas=[]
    for value in values:
        await crud.products.create_async(db,value)
        datas.append(value)
    return datas


@router.patch("/update/id")
async def update_product_by_id(id:str,update_model:ProductsUpdate,db:AsyncSession=Depends(get_session)):
    current_model=await crud.products.get_by_id_async(id,db)
    return await crud.products.update_async(db,current_model,update_model)


@router.delete("/delete/id")
async def delele_proudtc_by_id(id:str,db:AsyncSession=Depends(get_session)):
    return await crud.products.remove_async(db,id)