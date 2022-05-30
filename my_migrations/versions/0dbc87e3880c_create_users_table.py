"""create users table

Revision ID: 0dbc87e3880c
Revises: dccca138adb0
Create Date: 2022-05-30 16:54:18.854544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dbc87e3880c'
down_revision = 'dccca138adb0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("trust", sa.Integer(), nullable=False),
                    sa.Column("chat_id", sa.String(), nullable=False),
                    sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint('chat_id'),
                    sa.UniqueConstraint('chat_id')
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
