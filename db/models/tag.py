from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from db.models.associations import team_tags_association_table, tag_users_association_table


class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False, unique=True)
    teams: Mapped[List["Team"]] = relationship(back_populates='tags', secondary=team_tags_association_table)
    users: Mapped[List["User"]] = relationship(back_populates='tags', secondary=tag_users_association_table)