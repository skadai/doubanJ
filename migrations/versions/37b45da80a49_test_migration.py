"""test  migration

Revision ID: 37b45da80a49
Revises: 
Create Date: 2018-04-13 15:51:39.855394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b45da80a49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sk')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sk',
    sa.Column('id', sa.NUMERIC(), nullable=True),
    sa.Column('name', sa.TEXT(), nullable=True)
    )
    # ### end Alembic commands ###