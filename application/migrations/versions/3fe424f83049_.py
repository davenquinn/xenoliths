"""Created column for spot size

Revision ID: 3fe424f83049
Revises: 3162884275ae
Create Date: 2015-04-13 04:14:39.147790

"""

# revision identifiers, used by Alembic.
revision = '3fe424f83049'
down_revision = '3162884275ae'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('probe_measurement', sa.Column('spot_size', sa.Float(), nullable=True))


def downgrade():
    op.drop_column('probe_measurement', 'spot_size')
