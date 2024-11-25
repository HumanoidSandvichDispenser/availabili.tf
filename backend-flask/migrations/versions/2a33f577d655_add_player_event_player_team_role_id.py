"""Add player_event.player_team_role_id

Revision ID: 2a33f577d655
Revises: 2b05ba5ba9af
Create Date: 2024-11-24 16:29:03.546231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a33f577d655'
down_revision = '2b05ba5ba9af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players_events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('player_team_role_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_players_events_player_team_role_id_players_teams_roles', 'players_teams_roles', ['player_team_role_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players_events', schema=None) as batch_op:
        batch_op.drop_constraint('fk_players_events_player_team_role_id_players_teams_roles', type_='foreignkey')
        batch_op.drop_column('player_team_role_id')

    # ### end Alembic commands ###
