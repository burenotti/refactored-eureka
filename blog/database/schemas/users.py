import sqlalchemy as sa
from database.db import Base


class User(Base):

	__tablename__ = 'users'

	username = sa.Column('username', sa.String(32), primary_key=True)
	email = sa.Column('email', sa.String(128), nullable=False)
	password_hash = sa.Column('password_hash', sa.String(128), nullable=False)
	first_name = sa.Column('first_name', sa.String(32), nullable=False)
	last_name = sa.Column('last_name', sa.String(64), nullable=True)
