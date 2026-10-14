from app.crud.base import CRUDBase
from app.models.Products import Products
from app.schemas.products import ProductsCreate,ProductsUpdate


class CRUDProducts(CRUDBase[Products,ProductsCreate,ProductsUpdate]):
    pass

products=CRUDBase(Products)