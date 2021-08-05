"""users

Revision ID: f99b40a61441
Revises: 69d552c761f2
Create Date: 2019-11-24 00:46:11.569168

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f99b40a61441"
down_revision = "69d552c761f2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "misago_users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("slug", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("email_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=True),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_moderator", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("extra", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("email_hash"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(
        "misago_users_admins",
        "misago_users",
        ["is_admin"],
        unique=False,
        postgresql_where=sa.text("is_admin = true"),
    )
    op.create_index(
        "misago_users_inactive",
        "misago_users",
        ["is_active"],
        unique=False,
        postgresql_where=sa.text("is_active = false"),
    )
    op.create_index(
        "misago_users_moderators",
        "misago_users",
        ["is_moderator"],
        unique=False,
        postgresql_where=sa.text("is_moderator = true"),
    )
    op.create_index(
        "misago_users_without_full_names",
        "misago_users",
        ["full_name"],
        unique=False,
        postgresql_where=sa.text("full_name IS NULL"),
    )
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.create_index(
        "misago_users_full_names_search",
        "misago_users",
        ["full_name"],
        unique=False,
        postgresql_ops={"full_name": "gin_trgm_ops"},
        postgresql_using="gin",
    )
    op.create_index(
        "misago_users_slugs_search",
        "misago_users",
        ["slug"],
        unique=False,
        postgresql_ops={"slug": "gin_trgm_ops"},
        postgresql_using="gin",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("misago_users_moderators", table_name="misago_users")
    op.drop_index("misago_users_inactive", table_name="misago_users")
    op.drop_index("misago_users_admins", table_name="misago_users")
    op.drop_index("misago_users_slugs_search", table_name="misago_users")
    op.drop_index("misago_users_full_names_search", table_name="misago_users")
    op.drop_table("misago_users")
    # ### end Alembic commands ###
