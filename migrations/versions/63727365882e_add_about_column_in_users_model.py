"""Add about column in users model

Revision ID: 63727365882e
Revises: 460973688a95
Create Date: 2024-02-29 12:21:50.642936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63727365882e'
down_revision = '460973688a95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Feedback', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('about')

    with op.batch_alter_table('Feedback', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###