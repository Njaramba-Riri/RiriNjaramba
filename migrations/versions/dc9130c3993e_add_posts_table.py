"""Add Posts table

Revision ID: dc9130c3993e
Revises: 39a950cf2d1c
Create Date: 2024-01-25 08:12:36.543551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc9130c3993e'
down_revision = '39a950cf2d1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Blogs',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('post_author', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('post', sa.String(length=5000), nullable=False),
    sa.Column('tags', sa.String(length=100), nullable=False),
    sa.Column('updated', sa.Boolean(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('post_id')
    )
    with op.batch_alter_table('Blogs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Blogs_post_author'), ['post_author'], unique=True)
        batch_op.create_index(batch_op.f('ix_Blogs_title'), ['title'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Blogs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Blogs_title'))
        batch_op.drop_index(batch_op.f('ix_Blogs_post_author'))

    op.drop_table('Blogs')
    # ### end Alembic commands ###