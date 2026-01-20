"""Create JWKS table for Better Auth JWT plugin

Revision ID: 003
Revises: 002
Create Date: 2025-01-13

Better Auth JWT plugin requires this table to store JSON Web Key Sets.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create JWKS table for JWT plugin."""
    op.create_table(
        "jwks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("publicKey", sa.Text(), nullable=False),
        sa.Column("privateKey", sa.Text(), nullable=False),
        sa.Column("createdAt", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Drop JWKS table."""
    op.drop_table("jwks")
