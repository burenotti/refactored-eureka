"""User added

Revision ID: 8a7a2cad4f73
Revises: d476d54ac090
Create Date: 2021-09-23 13:14:12.885636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a7a2cad4f73'
down_revision = 'd476d54ac090'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
