import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..db import Base

__all__ = ["Post"]

class Post(Base):

	__tablename__ = "posts"

	# __mapper_args__ = {"eager_defaults": True}

	id = sa.Column("id", sa.Integer, primary_key=True)
	title = sa.Column("title", sa.String(120), nullable=False)
	creator_username = sa.Column("creator", sa.String, sa.ForeignKey("users.username"), nullable=False)
	creator = relationship("User")
	content = sa.Column("content", sa.Text, nullable=False)
