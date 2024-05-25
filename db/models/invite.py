from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import List
from enum import Enum
from db.models.associations import team_users_association_table, team_tags_association_table


class InviteStatus(Enum):
    CREATE = 'create'
    ACCEPT = 'accept'
    REJECT = 'reject'


class Invite(Base):
    __tablename__ = 'invites'
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    status: Mapped[InviteStatus] = mapped_column(default=InviteStatus.CREATE)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates='invitations')
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=False)
    team: Mapped["Team"] = relationship(back_populates='invitations')


