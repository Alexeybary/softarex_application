"""empty message

Revision ID: 72a87af2cb60
Revises: 3e19111705d6
Create Date: 2022-07-26 23:04:41.944572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72a87af2cb60'
down_revision = '3e19111705d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('info_table2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('count_of_dimension', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('info_table', 'lol')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('info_table', sa.Column('lol', sa.INTEGER(), nullable=True))
    op.drop_table('info_table2')
    # ### end Alembic commands ###
