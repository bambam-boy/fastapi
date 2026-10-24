from app.db.baseclass import Base
from sqlalchemy.orm import Mapped,mapped_column


class Users(Base):
    id:Mapped[int]=mapped_column(primary_key=True,nullable=False)
    username:Mapped[str]=mapped_column(nullable=False)
    email:Mapped[str]=mapped_column(nullable=False)
    hashed_password:Mapped[str]=mapped_column(nullable=False)
    is_active:Mapped[bool]=mapped_column(default=False)
    is_verfide:Mapped[bool]=mapped_column(default=False)