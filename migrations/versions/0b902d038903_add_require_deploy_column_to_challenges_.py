"""Add require_deploy column to Challenges model

Revision ID: 0b902d038903
Revises: a02c5bf43407
Create Date: 2024-10-14 13:49:12.695858

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0b902d038903"
down_revision = "a02c5bf43407"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "deploy_challenge",
        sa.Column("image_name", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "deploy_challenge", sa.Column("time_limit", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "deploy_challenge", sa.Column("last_update", sa.DateTime(), nullable=True)
    )
    op.create_unique_constraint(None, "deploy_challenge", ["image_name"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "deploy_challenge", type_="unique")
    op.drop_column("deploy_challenge", "last_update")
    op.drop_column("deploy_challenge", "time_limit")
    op.drop_column("deploy_challenge", "image_name")
    # ### end Alembic commands ###
