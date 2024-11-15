"""Add PlayerTeam.is_team_leader

Revision ID: f50a79c4ae22
Revises: ea359b0e46d7
Create Date: 2024-11-03 17:11:35.956743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f50a79c4ae22'
down_revision = 'ea359b0e46d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players_teams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_team_leader', sa.Boolean(), nullable=False, server_default='0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players_teams', schema=None) as batch_op:
        batch_op.drop_column('is_team_leader')

    # ### end Alembic commands ###
