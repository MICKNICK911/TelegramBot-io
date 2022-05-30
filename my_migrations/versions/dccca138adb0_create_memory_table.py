"""create memory table

Revision ID: dccca138adb0
Revises: 
Create Date: 2022-05-30 16:51:30.915346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dccca138adb0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("memory",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("listen", sa.String(), nullable=False),
                    sa.Column("reply", sa.String(), nullable=False),
                    sa.Column("Author", sa.String(), nullable=False),
                    sa.Column("published", sa.Boolean(), nullable=False, server_default='FALSE'),
                    sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text("now()"))
                    )
    pass


def downgrade():
    op.drop_table("memory")
    pass
