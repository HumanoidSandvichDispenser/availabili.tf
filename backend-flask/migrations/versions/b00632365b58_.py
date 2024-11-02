"""empty message

Revision ID: b00632365b58
Revises: a340b3da0f2a
Create Date: 2024-10-29 23:27:37.306568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b00632365b58'
down_revision = 'a340b3da0f2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_sessions',
    sa.Column('key', sa.String(length=31), nullable=False),
    sa.Column('player_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['player_id'], ['players.steam_id'], ),
    sa.PrimaryKeyConstraint('key')
    )
    op.drop_table('auth_session')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_session',
    sa.Column('player_id', sa.BIGINT(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('key', sa.VARCHAR(length=31), nullable=False),
    sa.ForeignKeyConstraint(['player_id'], ['players.steam_id'], ),
    sa.PrimaryKeyConstraint('player_id')
    )
    op.drop_table('auth_sessions')
    # ### end Alembic commands ###
