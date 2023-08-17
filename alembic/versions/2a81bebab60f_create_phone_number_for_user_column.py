"""Create phone number for user column

Revision ID: 2a81bebab60f
Revises: 
Create Date: 2023-08-17 08:01:55.650989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a81bebab60f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
