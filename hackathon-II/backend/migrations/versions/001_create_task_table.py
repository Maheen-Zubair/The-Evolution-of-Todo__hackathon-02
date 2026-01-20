"""Create task table with indexes

Revision ID: 001
Revises:
Create Date: 2025-01-07

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create task table with indexes."""
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("is_complete", sa.Boolean(), nullable=False, default=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    # Create indexes for common query patterns
    op.create_index("ix_task_user_id", "task", ["user_id"])
    op.create_index("idx_task_user_complete", "task", ["user_id", "is_complete"])
    op.create_index("idx_task_user_created", "task", ["user_id", "created_at"])


def downgrade() -> None:
    """Drop task table and indexes."""
    op.drop_index("idx_task_user_created", table_name="task")
    op.drop_index("idx_task_user_complete", table_name="task")
    op.drop_index("ix_task_user_id", table_name="task")
    op.drop_table("task")
