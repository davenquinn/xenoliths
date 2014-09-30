"""Rename table `point` to `probe_measurement`

Revision ID: 3a028a18a9fb
Revises: 467d24bf1e2c
Create Date: 2014-09-30 00:51:08.109257

"""

# revision identifiers, used by Alembic.
revision = '3a028a18a9fb'
down_revision = '467d24bf1e2c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.rename_table("point","probe_measurement")

def downgrade():
    op.rename_table("probe_measurement","point")
