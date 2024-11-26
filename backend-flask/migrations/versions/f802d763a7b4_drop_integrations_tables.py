"""Drop integrations tables

Revision ID: f802d763a7b4
Revises: dcf5ffd0ec73
Create Date: 2024-11-25 18:34:08.136071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f802d763a7b4'
down_revision = 'dcf5ffd0ec73'
branch_labels = None
depends_on = None


def upgrade():
    # drop integrations tables
    op.drop_table("team_discord_integrations")
    op.drop_table("team_logs_tf_integrations")
    op.drop_table("team_integrations")
    pass


def downgrade():
    pass
