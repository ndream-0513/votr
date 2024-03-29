"""add close_date in Topics Model

Revision ID: d7d46fc3d825
Revises: 68c833c5a316
Create Date: 2024-03-12 22:04:48.848697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7d46fc3d825'
down_revision = '68c833c5a316'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.add_column(sa.Column('close_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.drop_column('close_date')

    # ### end Alembic commands ###
