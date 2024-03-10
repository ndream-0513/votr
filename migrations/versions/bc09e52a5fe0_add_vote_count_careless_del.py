"""add vote_count(careless del)

Revision ID: bc09e52a5fe0
Revises: 3942c7bea6d0
Create Date: 2024-03-10 08:46:41.866611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc09e52a5fe0'
down_revision = '3942c7bea6d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('polls', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vote_count', sa.Integer(), nullable=True))
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('polls', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('vote_count')

    # ### end Alembic commands ###