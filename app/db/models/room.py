from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from app.db import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(unique=True)
    name: Mapped[Optional[str]] = mapped_column((String(50)), nullable=True)
    img_url: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    img_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    img_name_orig: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_reserved: Mapped[bool] = mapped_column(Boolean(), default=False)

    def __str__(self):
        return f"Номер кімнати № {self.number}: {self.name}"
