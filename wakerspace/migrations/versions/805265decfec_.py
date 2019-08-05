"""empty message

Revision ID: 805265decfec
Revises: 
Create Date: 2019-08-04 14:09:35.468108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '805265decfec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('staff',
    sa.Column('maker_id', sa.Integer(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['maker_id'], ['maker.id'], ),
    sa.PrimaryKeyConstraint('maker_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('staff')
    # ### end Alembic commands ###