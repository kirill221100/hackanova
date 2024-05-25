from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String
from enum import Enum
from db.models.associations import team_users_association_table, tag_users_association_table
from db.models.team import Team


class UserTeamStatus(Enum):
    IN_TEAM = 'in-team'
    NOT_IN_TEAM = 'not-in-team'


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    experience: Mapped[str] = mapped_column(nullable=True)
    education: Mapped[str] = mapped_column(nullable=True)
    about_me: Mapped[str] = mapped_column(nullable=True)
    hackathon_search: Mapped[bool] = mapped_column(default=True)
    job_search: Mapped[bool] = mapped_column(default=False)
    status_team: Mapped[UserTeamStatus] = mapped_column(nullable=False, default=UserTeamStatus.NOT_IN_TEAM.value)
    avatar: Mapped[str] = mapped_column(nullable=True)
    invitations: Mapped[List["Invite"]] = relationship(back_populates='user')
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=tag_users_association_table, back_populates="users")
    teams: Mapped[List["Team"]] = relationship("Team", secondary=team_users_association_table, back_populates="participants")  # Отношение к командам через ассоциативную таблицу

