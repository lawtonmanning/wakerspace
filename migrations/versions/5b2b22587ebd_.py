"""empty message

Revision ID: 5b2b22587ebd
Revises: 7d1179db7d5a
Create Date: 2019-09-02 12:30:50.896540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b2b22587ebd'
down_revision = '7d1179db7d5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('name', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activity', 'name')
    # ### end Alembic commands ###
