"""Add about column in users model

Revision ID: 460973688a95
Revises: a9073772aa77
Create Date: 2024-02-29 12:15:46.864015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '460973688a95'
down_revision = 'a9073772aa77'
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