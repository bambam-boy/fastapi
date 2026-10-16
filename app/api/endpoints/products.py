from fastapi.routing import APIRouter
from app import crud
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.products import ProductsCreate,ProductsUpdate
from redis_fastapi import cache,cache_evict,rate_limit


router=APIRouter()


@router.get(
    "/get/multi",
    dependencies=[
        Depends(rate_limit("50/minute")),
        Depends(cache(eviction_group="products",ttl=600))
    ]
)
async def get_multi_products(db:AsyncSession=Depends(get_session),skip:int=0,limit:int=100,asc:bool=False):
    return await crud.products.get_multi_async(db,skip,limit,asc)


@router.get(
    "/get/price",    
    dependencies=[
        Depends(rate_limit("50/minute")),
        Depends(cache(eviction_group="products",ttl=600))
    ]
)
async def get_products_by_price(db:AsyncSession=Depends(get_session),skip:int=0,limit:int=100,asc:bool=False,max:int=1000000):
    return await crud.products.get_products_by_price_async(db,max,skip,limit,asc)


@router.get(
    "/get/name",    
    dependencies=[
        Depends(rate_limit("50/minute")),
        Depends(cache(eviction_group="products",ttl=600))
    ]
)
async def get_products_by_name(name:str,db:AsyncSession=Depends(get_session),skip:int=0,limit:int=100):
    return await crud.products.get_products_be_name_async(db,name,skip,limit)


@router.get(
    "/get/id",
    dependencies=[
        Depends(rate_limit("50/minute",on_limit_exceeded={"hint":"too many reqs from you wait a bit"})),
        Depends(cache(eviction_group="products",ttl=600))
    ]
)
async def get_product_by_id(id:str,db:AsyncSession=Depends(get_session)):
    return await crud.products.get_by_id_async(id,db)


@router.post(
    "/add/single",
    dependencies=[
        Depends(rate_limit("25/minute")),
        Depends(cache_evict(eviction_group="products"))
    ]
)
async def insert_single_product(value:ProductsCreate,db:AsyncSession=Depends(get_session)):
    return await crud.products.create_async(db,value)


@router.post(
    "/add/multi",
    dependencies=[
        Depends(rate_limit("25/minute")),
        Depends(cache_evict(eviction_group="products"))
    ]
)
async def insert_multi_products(values:list[ProductsCreate],db:AsyncSession=Depends(get_session)):
    datas=[]
    for value in values:
        await crud.products.create_async(db,value)
        datas.append(value)
    return datas


@router.patch(
    "/update/id",
    dependencies=[
        Depends(rate_limit("25/minute")),
        Depends(cache_evict(eviction_group="products"))
    ]
)
async def update_product_by_id(id:str,update_model:ProductsUpdate,db:AsyncSession=Depends(get_session)):
    current_model=await crud.products.get_by_id_async(id,db)
    return await crud.products.update_async(db,current_model,update_model)


@router.delete(
    "/delete/id",
    dependencies=[
        Depends(rate_limit("25/minute")),
        Depends(cache_evict(eviction_group="products"))
    ]
)
async def delele_proudtc_by_id(id:str,db:AsyncSession=Depends(get_session)):
    return await crud.products.remove_async(db,id)


