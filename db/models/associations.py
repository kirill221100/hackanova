from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from db.db_setup import Base


team_users_association_table = Table(
    "team_users_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
)

team_tags_association_table = Table(
    "team_tags_association_table",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
)


tag_users_association_table = Table(
    "tag_users_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

contact_users_association_table = Table(
    "contact_users_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
)
