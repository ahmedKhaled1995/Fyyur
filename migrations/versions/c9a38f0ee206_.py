"""empty message

Revision ID: c9a38f0ee206
Revises: 0ad37c51d886
Create Date: 2020-09-22 15:31:06.549768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9a38f0ee206'
down_revision = '0ad37c51d886'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'genres')
    # ### end Alembic commands ###
