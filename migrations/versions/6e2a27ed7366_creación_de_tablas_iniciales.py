"""Creación de tablas iniciales

Revision ID: 6e2a27ed7366
Revises: 
Create Date: 2026-03-01 14:28:43.922832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6e2a27ed7366'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('scooter')
    op.drop_table('zone')

def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'zone',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.VARCHAR(), nullable=False),
        sa.Column('codigo_postal', sa.INTEGER(), nullable=False),
        sa.Column('limite_velocidad', sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('zone_pkey'))
    )

    op.create_table(
        'scooter',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('numero_serie', sa.VARCHAR(), nullable=False),
        sa.Column('modelo', sa.VARCHAR(), nullable=False),
        sa.Column('bateria', sa.INTEGER(), nullable=False),
        sa.Column(
            'estado',
            postgresql.ENUM(
                'disponible',
                'en_uso',
                'mantenimiento',
                'sin_bateria',
                name='scooterstatus'
            ),
            nullable=False
        ),
        sa.Column('zona_id', sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(['zona_id'], ['zone.id'], name=op.f('scooter_zona_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('scooter_pkey')),
        sa.UniqueConstraint('numero_serie', name=op.f('scooter_numero_serie_key'))
    )
