import uuid
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.baseclass import Base


class Products(Base):
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name:Mapped[str]=mapped_column(nullable=False)
    price:Mapped[int]=mapped_column(nullable=False)
    count:Mapped[int]=mapped_column(nullable=False)