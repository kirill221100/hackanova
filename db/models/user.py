from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class User(Base):
    __tablename__ = 'users'

