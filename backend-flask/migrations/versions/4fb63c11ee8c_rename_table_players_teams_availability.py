"""Rename table players_teams_availability

Revision ID: 4fb63c11ee8c
Revises: 8ea29cf493f5
Create Date: 2024-10-30 22:45:51.227298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fb63c11ee8c'
down_revision = '8ea29cf493f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players_teams_availability',
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['player_id', 'team_id'], ['players_teams.player_id', 'players_teams.team_id'], ),
    sa.PrimaryKeyConstraint('player_id', 'team_id', 'start_time')
    )
    op.drop_table('player_team_availability')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player_team_availability',
    sa.Column('player_id', sa.INTEGER(), nullable=False),
    sa.Column('team_id', sa.INTEGER(), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['player_id', 'team_id'], ['players_teams.player_id', 'players_teams.team_id'], ),
    sa.PrimaryKeyConstraint('player_id', 'team_id')
    )
    op.drop_table('players_teams_availability')
    # ### end Alembic commands ###
