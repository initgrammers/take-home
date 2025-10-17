"""init schema

Revision ID: b26b25433f1a
Revises: 
Create Date: 2025-10-17 15:28:35.923057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b26b25433f1a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create base tables for rooms, reservations, and payments."""
    # rooms table
    op.create_table(
        'rooms',
        sa.Column('id', sa.String(length=36), primary_key=True, index=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('price_per_night', sa.Numeric(10, 2), nullable=False),
    )

    # reservations table
    op.create_table(
        'reservations',
        sa.Column('id', sa.String(length=36), primary_key=True, index=True),
        sa.Column('room_id', sa.String(length=36), nullable=False, index=True),
        sa.Column('guest_email', sa.String(length=100), nullable=False, index=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default=sa.text("'active'")),
    )

    # payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.String(length=36), primary_key=True, index=True),
        sa.Column('reservation_id', sa.String(length=36), nullable=False, index=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
    )


def downgrade() -> None:
    """Drop base tables."""
    op.drop_table('payments')
    op.drop_table('reservations')
    op.drop_table('rooms')
