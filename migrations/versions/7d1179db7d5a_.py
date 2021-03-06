"""empty message

Revision ID: 7d1179db7d5a
Revises: 
Create Date: 2019-09-02 12:27:03.393872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d1179db7d5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('color',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=6), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('value')
    )
    op.create_table('maker',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('rfid', sa.Integer(), nullable=True),
    sa.Column('classification', sa.Enum('STUDENT', 'FACULTY', 'STAFF', 'RESEARCHER', name='classification'), nullable=False),
    sa.Column('year', sa.Enum('FRESHMAN', 'SOPHOMORE', 'JUNIOR', 'SENIOR', 'GRADUATE', name='year'), nullable=True),
    sa.Column('staff', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('rfid')
    )
    op.create_table('training_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('color_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['color_id'], ['color.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('training_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['training_type_id'], ['training_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('training',
    sa.Column('maker_id', sa.Integer(), nullable=False),
    sa.Column('training_type_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['maker_id'], ['maker.id'], ),
    sa.ForeignKeyConstraint(['training_type_id'], ['training_type.id'], ),
    sa.PrimaryKeyConstraint('maker_id', 'training_type_id')
    )
    op.create_table('visit',
    sa.Column('maker_id', sa.Integer(), nullable=False),
    sa.Column('in_time', sa.DateTime(), nullable=False),
    sa.Column('out_time', sa.DateTime(), nullable=True),
    sa.Column('purpose', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['maker_id'], ['maker.id'], ),
    sa.ForeignKeyConstraint(['purpose'], ['activity.id'], ),
    sa.PrimaryKeyConstraint('maker_id', 'in_time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visit')
    op.drop_table('training')
    op.drop_table('activity')
    op.drop_table('training_type')
    op.drop_table('maker')
    op.drop_table('color')
    # ### end Alembic commands ###
