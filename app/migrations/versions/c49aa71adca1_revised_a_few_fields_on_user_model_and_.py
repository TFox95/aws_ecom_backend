"""revised a few fields on User model. And added lengths on the fields which are strings.

Revision ID: c49aa71adca1
Revises: 
Create Date: 2024-05-29 11:52:24.207221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c49aa71adca1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
