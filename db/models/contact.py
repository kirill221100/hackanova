from sqlalchemy import ForeignKey

from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    VK: Mapped[int] = mapped_column(nullable=True)
    Github: Mapped[int] = mapped_column(nullable=True)
    Telegram: Mapped[int] = mapped_column(nullable=True)
