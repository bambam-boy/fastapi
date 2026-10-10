from typing import Any
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    id:Any
    __name__:str


    @declared_attr
    def __tablename__(cls)->str:
        return cls.__name__.lower()


    create_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow)
    mod_at:Mapped[datetime]=mapped_column(
        DateTime,
        onupdate=datetime.utcnow,
        default=datetime.utcnow)
