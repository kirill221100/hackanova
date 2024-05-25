from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from db.models.associations import team_users_association_table, team_tags_association_table


class Team(Base):
    __tablename__ = 'teams'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    commandDescription: Mapped[str] = mapped_column(nullable=False)
    task: Mapped[str] = mapped_column(nullable=False)
    tags: Mapped[List["Tag"]] = relationship(back_populates='teams', secondary=team_tags_association_table)
    participants: Mapped[List["User"]] = relationship(back_populates='commands', secondary=team_users_association_table)
