"""Adding probe image.

Revision ID: 3e9198a5c790
Revises: 53d79fe4c042
Create Date: 2015-01-08 10:09:32.498950

"""

# revision identifiers, used by Alembic.
revision = '3e9198a5c790'
down_revision = '53d79fe4c042'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('probe_image',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('x_min', sa.Float(), nullable=True),
        sa.Column('x_max', sa.Float(), nullable=True),
        sa.Column('y_min', sa.Float(), nullable=True),
        sa.Column('y_max', sa.Float(), nullable=True),
        sa.Column('magnification', sa.Float(), nullable=True),
        sa.Column('sample_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['sample_id'], ['sample.id'], ),
        sa.PrimaryKeyConstraint('id'))

def downgrade():
    op.drop_table('probe_image')
