from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from db.models.associations import team_users_association_table, team_tags_association_table
from enum import Enum


class TeamStatus(Enum):
    COMPLETE = 'complete'
    NOT_COMPLETE = 'not-complete'


class Team(Base):
    __tablename__ = 'teams'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    team_description: Mapped[str] = mapped_column(nullable=False)
    search_user_description: Mapped[str] = mapped_column(nullable=False)
    task: Mapped[str] = mapped_column(nullable=False)
    tags: Mapped[List["Tag"]] = relationship(back_populates='teams', secondary=team_tags_association_table)
    status: Mapped[TeamStatus] = mapped_column(default=TeamStatus.NOT_COMPLETE, nullable=False)
    participants: Mapped[List["User"]] = relationship(back_populates='teams', secondary=team_users_association_table)
    invitations: Mapped[List["Invite"]] = relationship(back_populates='team')

