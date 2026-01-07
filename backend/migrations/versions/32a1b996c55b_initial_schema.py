"""Initial schema

Revision ID: 32a1b996c55b
Revises: 
Create Date: 2026-01-06 18:23:29.739380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32a1b996c55b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Repositories
    op.create_table(
        'repositories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('gitlab_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('path_with_namespace', sa.String(length=500), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('gitlab_id')
    )

    # Commits
    op.create_table(
        'commits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sha', sa.String(length=100), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('author_name', sa.String(length=255), nullable=False),
        sa.Column('author_email', sa.String(length=255), nullable=False),
        sa.Column('authored_date', sa.DateTime(), nullable=False),
        sa.Column('repository_id', sa.Integer(), nullable=False),
        sa.Column('jira_key', sa.String(length=50), nullable=True),
        sa.Column('stats', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['repository_id'], ['repositories.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sha')
    )
    op.create_index(op.f('ix_commits_jira_key'), 'commits', ['jira_key'], unique=False)

    # Merge Requests
    op.create_table(
        'merge_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('gitlab_id', sa.Integer(), nullable=False),
        sa.Column('iid', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('state', sa.String(length=50), nullable=False),
        sa.Column('author_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('merged_at', sa.DateTime(), nullable=True),
        sa.Column('repository_id', sa.Integer(), nullable=False),
        sa.Column('jira_key', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['repository_id'], ['repositories.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('gitlab_id')
    )
    op.create_index(op.f('ix_merge_requests_jira_key'), 'merge_requests', ['jira_key'], unique=False)

    # Jira Issues
    op.create_table(
        'jira_issues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=50), nullable=False),
        sa.Column('summary', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=100), nullable=False),
        sa.Column('issue_type', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.Column('assignee', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('resolution_date', sa.DateTime(), nullable=True),
        sa.Column('status_history', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    op.create_index(op.f('ix_jira_issues_key'), 'jira_issues', ['key'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_jira_issues_key'), table_name='jira_issues')
    op.drop_table('jira_issues')
    op.drop_index(op.f('ix_merge_requests_jira_key'), table_name='merge_requests')
    op.drop_table('merge_requests')
    op.drop_index(op.f('ix_commits_jira_key'), table_name='commits')
    op.drop_table('commits')
    op.drop_table('repositories')
