from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import List
from enum import Enum


class InviteStatus(Enum):
    WAITING = 'waiting'
    ACCEPT = 'accept'
    REJECT = 'reject'


class InviteType(Enum):
    TO_USER = 'to-user'
    TO_TEAM = 'to-team'


class Invite(Base):
    __tablename__ = 'invitations'
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    status: Mapped[InviteStatus] = mapped_column(default=InviteStatus.WAITING)
    type: Mapped[InviteType] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates='invitations')
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=False)
    team: Mapped["Team"] = relationship(back_populates='invitations')


