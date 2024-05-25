from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String

from db.models.associations import team_users_association_table
from db.models.team import Team


class User(Base):
    __tableName__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(nullable=True)
    experience: Mapped[str] = mapped_column(nullable=True)
    education: Mapped[str] = mapped_column(nullable=True)
    about_me: Mapped[str] = mapped_column(nullable=True)
    status_team: Mapped[bool] = mapped_column(nullable=False, default=False)
    hashtags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    teams: Mapped[List["Team"]] = relationship("Team", secondary=team_users_association_table, back_populates="users")  # Отношение к командам через ассоциативную таблицу

