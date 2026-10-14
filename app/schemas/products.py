from pydantic import BaseModel


class ProductsBase(BaseModel):
    name:str
    price:int
    count:int

class ProductsCreate(ProductsBase):
    pass


class ProductsUpdate(ProductsBase):
    name:str|None=None
    price:int|None=None
    count:int|None=None
