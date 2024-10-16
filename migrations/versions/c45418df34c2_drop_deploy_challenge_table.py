"""Drop deploy_challenge table

Revision ID: c45418df34c2
Revises: 15770b4b62c0
Create Date: 2024-10-14 15:09:04.799263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45418df34c2'
down_revision = '15770b4b62c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deploy_challenge', sa.Column('image_name', sa.String(length=128), nullable=True))
    op.add_column('deploy_challenge', sa.Column('time_limit', sa.DateTime(), nullable=True))
    op.add_column('deploy_challenge', sa.Column('last_update', sa.DateTime(), nullable=True))
    op.create_unique_constraint(None, 'deploy_challenge', ['image_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'deploy_challenge', type_='unique')
    op.drop_column('deploy_challenge', 'last_update')
    op.drop_column('deploy_challenge', 'time_limit')
    op.drop_column('deploy_challenge', 'image_name')
    # ### end Alembic commands ###
