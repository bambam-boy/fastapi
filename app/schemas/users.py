from pydantic import BaseModel


class UsersBase(BaseModel):
    username:str
    email:str
    password:str


class UsersCreate(UsersBase):
    email:str | None=None


class UsersUpdate(UsersBase):
    useranme:str|None=None
    email:str|None=None
    password:str|None=None


class UsersResponcePublic(BaseModel):
    username:str


class UsersResponcePrivete(UsersResponcePublic):
    email:str