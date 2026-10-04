"""add user id to notification

Revision ID: 9cf573ce3b2d
Revises: 1a3ab9a2b26f
Create Date: 2026-10-02 16:16:33.968170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cf573ce3b2d'
down_revision: Union[str, Sequence[str], None] = '1a3ab9a2b26f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DELETE FROM notifications")
    with op.batch_alter_table("notifications") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            "fk_notifications_user_id", "users", ["user_id"], ["id"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("notifications") as batch_op:
        batch_op.drop_constraint("fk_notifications_user_id", type_="foreignkey")
        batch_op.drop_column("user_id")
