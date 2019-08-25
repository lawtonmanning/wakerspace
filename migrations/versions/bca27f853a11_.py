"""empty message

Revision ID: bca27f853a11
Revises: 2a7bcda71ae3
Create Date: 2019-08-24 15:15:18.808794

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bca27f853a11'
down_revision = '2a7bcda71ae3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equipment', sa.Column('room_id', sa.Integer(), nullable=False))
    op.drop_constraint('equipment_ibfk_1', 'equipment', type_='foreignkey')
    op.create_foreign_key(None, 'equipment', 'room', ['room_id'], ['id'])
    op.drop_column('equipment', 'room')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equipment', sa.Column('room', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'equipment', type_='foreignkey')
    op.create_foreign_key('equipment_ibfk_1', 'equipment', 'room', ['room'], ['id'])
    op.drop_column('equipment', 'room_id')
    # ### end Alembic commands ###
