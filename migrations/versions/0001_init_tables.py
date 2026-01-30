from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "articles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.String, unique=True, index=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("body_md", sa.Text, nullable=False),
        sa.Column("published_at", sa.String, nullable=True),
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.String, unique=True, index=True, nullable=False),
        sa.Column("name", sa.String, nullable=False),
    )

    op.create_table(
        "article_tags",
        sa.Column(
            "article_id",
            sa.Integer,
            sa.ForeignKey("articles.id"),
            primary_key=True,
        ),
        sa.Column(
            "tag_id",
            sa.Integer,
            sa.ForeignKey("tags.id"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("article_tags")
    op.drop_table("tags")
    op.drop_table("articles")
