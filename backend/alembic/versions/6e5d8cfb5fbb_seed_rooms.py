"""seed rooms

Revision ID: 6e5d8cfb5fbb
Revises: b26b25433f1a
Create Date: 2025-10-17 15:34:48.145330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e5d8cfb5fbb'
down_revision: Union[str, Sequence[str], None] = 'b26b25433f1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_ROOMS = [
    {"id": "7c79f442-fde0-4ef2-9eeb-0dffe92b3a0e", "name": "room1", "price_per_night": 80.0},
    {"id": "df2a67e2-cd30-42de-b3be-ee3d4fc24652", "name": "room2", "price_per_night": 90.0},
    {"id": "e4ec572e-fc15-44a8-bde5-8e692acf9279", "name": "room3", "price_per_night": 100.0},
]


def upgrade() -> None:
    """Insert seed rooms idempotently (Postgres and SQLite supported)."""
    conn = op.get_bind()
    dialect = conn.dialect.name

    if dialect == "postgresql":
        # Use ON CONFLICT DO NOTHING to keep idempotency
        for r in SEED_ROOMS:
            conn.execute(
                sa.text(
                    """
                    INSERT INTO rooms (id, name, price_per_night)
                    VALUES (:id, :name, :price)
                    ON CONFLICT (id) DO NOTHING
                    """
                ),
                {"id": r["id"], "name": r["name"], "price": r["price_per_night"]},
            )
    elif dialect == "sqlite":
        # SQLite syntax for idempotent insert
        for r in SEED_ROOMS:
            conn.execute(
                sa.text(
                    """
                    INSERT OR IGNORE INTO rooms (id, name, price_per_night)
                    VALUES (:id, :name, :price)
                    """
                ),
                {"id": r["id"], "name": r["name"], "price": r["price_per_night"]},
            )
    else:
        # Fallback: check existence before insert
        for r in SEED_ROOMS:
            exists = conn.execute(
                sa.text("SELECT 1 FROM rooms WHERE id = :id"),
                {"id": r["id"]},
            ).fetchone()
            if not exists:
                conn.execute(
                    sa.text(
                        "INSERT INTO rooms (id, name, price_per_night) VALUES (:id, :name, :price)"
                    ),
                    {"id": r["id"], "name": r["name"], "price": r["price_per_night"]},
                )


def downgrade() -> None:
    """Remove seeded rooms by id."""
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "DELETE FROM rooms WHERE id IN (:id1, :id2, :id3)"
        ),
        {
            "id1": SEED_ROOMS[0]["id"],
            "id2": SEED_ROOMS[1]["id"],
            "id3": SEED_ROOMS[2]["id"],
        },
    )
