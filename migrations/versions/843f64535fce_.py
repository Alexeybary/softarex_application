"""empty message

Revision ID: 843f64535fce
Revises: 7b3033ea61b6
Create Date: 2022-07-25 23:47:17.856195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843f64535fce'
down_revision = '7b3033ea61b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dimension', sa.Column('dimension_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dimension', 'dimension_name')
    # ### end Alembic commands ###
