"""empty message

Revision ID: 1c26af57c200
Revises: 45000f7cf873
Create Date: 2014-12-09 22:13:31.190922

"""

# revision identifiers, used by Alembic.
revision = '1c26af57c200'
down_revision = '45000f7cf873'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('probe_measurement', sa.Column('location', Geometry(geometry_type='POINT'), nullable=True))
    op.drop_column('probe_measurement', 'molar')
    op.drop_column('probe_measurement', 'oxides')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('probe_measurement', sa.Column('oxides', postgresql.JSON(), autoincrement=False, nullable=True))
    op.add_column('probe_measurement', sa.Column('molar', postgresql.JSON(), autoincrement=False, nullable=True))
    op.drop_column('probe_measurement', 'location')

    ### end Alembic commands ###
