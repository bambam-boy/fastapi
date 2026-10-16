from app.crud.base import CRUDBase
from app.models.Products import Products
from app.schemas.products import ProductsCreate,ProductsUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_session
from sqlalchemy import select


class CRUDProducts(CRUDBase[Products,ProductsCreate,ProductsUpdate]):
    async def get_products_by_price_async(
        self,
        db:AsyncSession=Depends(get_session),
        price:int=1,
        skip:int=0,
        limit:int=100,
        asc:bool=False
    ):
        query=(
            select(Products).
            where(Products.price<=price).
            order_by(Products.price.asc() if asc else Products.price.desc()).
            offset(skip)
        )

        if limit is None:
            return await self.get_all(db.scalars(query))
        return await self.get_all(db.scalars(query.limit(limit)))


    async def get_products_be_name_async(
        self,
        db:AsyncSession=Depends(get_session),
        name:str="",
        skip:int=0,
        limit:int=100,
    ):
        query=(
            select(Products).
            where(Products.name==name).
            offset(skip)
        )

        if limit is None:
            return await self.get_all(db.scalars(query))
        return await self.get_all(db.scalars(query.limit(limit)))

products=CRUDProducts(Products)