"""Make player role primary key

Revision ID: 2b2f3ae2ec7f
Revises: 958df14798d5
Create Date: 2024-10-31 19:07:02.960849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b2f3ae2ec7f'
down_revision = '958df14798d5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('players_teams_roles', schema=None) as batch_op:
        batch_op.create_primary_key('pk_players_teams_roles', ['player_id', 'team_id', 'role'])


def downgrade():
    with op.batch_alter_table('players_teams_roles', schema=None) as batch_op:
        batch_op.drop_constraint('pk_players_teams_roles')
