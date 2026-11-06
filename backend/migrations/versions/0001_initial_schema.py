"""Initial ARAM schema.

Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

application_status = sa.Enum(
    "APPLIED", "RECEIVED", "IN_REVIEW", "INTERVIEW", "TECHNICAL_TEST",
    "REJECTED", "OFFER", "WITHDRAWN", "CLOSED", "UNKNOWN",
    name="application_status",
    create_type=False,
)


def upgrade():
    bind = op.get_bind()
    application_status.create(bind, checkfirst=True)

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company", sa.String(255), nullable=False),
        sa.Column("role_title", sa.String(255), nullable=False),
        sa.Column("salary_rate", sa.String(100)),
        sa.Column("job_advert_url", sa.Text()),
        sa.Column("application_date", sa.Date()),
        sa.Column("contact_name", sa.String(255)),
        sa.Column("contact_email", sa.String(320)),
        sa.Column("contact_phone", sa.String(80)),
        sa.Column("response_status_raw", sa.Text()),
        sa.Column("interview_stage", sa.String(255)),
        sa.Column("interview_at", sa.DateTime(timezone=True)),
        sa.Column("interviewer_name", sa.String(255)),
        sa.Column("offer_status_raw", sa.String(100)),
        sa.Column("status", application_status, nullable=False, server_default="APPLIED"),
        sa.Column("spreadsheet_tab", sa.String(255)),
        sa.Column("spreadsheet_row_id", sa.String(255), unique=True),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_applications_company", "applications", ["company"])
    op.create_index("ix_applications_role_title", "applications", ["role_title"])
    op.create_index("ix_applications_status", "applications", ["status"])

    op.create_table(
        "email_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("gmail_message_id", sa.String(255), nullable=False, unique=True),
        sa.Column("gmail_thread_id", sa.String(255)),
        sa.Column("sender", sa.String(320)),
        sa.Column("subject", sa.Text()),
        sa.Column("received_at", sa.DateTime(timezone=True)),
        sa.Column("event_type", sa.String(80)),
        sa.Column("confidence", sa.Float()),
        sa.Column("processing_status", sa.String(40), nullable=False, server_default="NEW"),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id", ondelete="SET NULL")),
        sa.Column("snippet", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_email_events_gmail_thread_id", "email_events", ["gmail_thread_id"])
    op.create_index("ix_email_events_event_type", "email_events", ["event_type"])
    op.create_index("ix_email_events_processing_status", "email_events", ["processing_status"])

    op.create_table(
        "status_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id", ondelete="CASCADE"), nullable=False),
        sa.Column("old_status", sa.String(40)),
        sa.Column("new_status", sa.String(40), nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("source", sa.String(40), nullable=False, server_default="MANUAL"),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_status_history_application_id", "status_history", ["application_id"])

    op.create_table(
        "pending_actions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id", ondelete="SET NULL")),
        sa.Column("email_event_id", sa.Integer(), sa.ForeignKey("email_events.id", ondelete="SET NULL")),
        sa.Column("action_type", sa.String(80), nullable=False),
        sa.Column("proposed_changes", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float()),
        sa.Column("status", sa.String(40), nullable=False, server_default="PENDING"),
        sa.Column("review_note", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_pending_actions_application_id", "pending_actions", ["application_id"])
    op.create_index("ix_pending_actions_email_event_id", "pending_actions", ["email_event_id"])
    op.create_index("ix_pending_actions_status", "pending_actions", ["status"])

    op.create_table(
        "sync_state",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("integration", sa.String(80), nullable=False, unique=True),
        sa.Column("cursor", sa.Text()),
        sa.Column("last_success_at", sa.DateTime(timezone=True)),
        sa.Column("last_error", sa.Text()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("sync_state")
    op.drop_index("ix_pending_actions_status", table_name="pending_actions")
    op.drop_index("ix_pending_actions_email_event_id", table_name="pending_actions")
    op.drop_index("ix_pending_actions_application_id", table_name="pending_actions")
    op.drop_table("pending_actions")
    op.drop_index("ix_status_history_application_id", table_name="status_history")
    op.drop_table("status_history")
    op.drop_index("ix_email_events_processing_status", table_name="email_events")
    op.drop_index("ix_email_events_event_type", table_name="email_events")
    op.drop_index("ix_email_events_gmail_thread_id", table_name="email_events")
    op.drop_table("email_events")
    op.drop_index("ix_applications_status", table_name="applications")
    op.drop_index("ix_applications_role_title", table_name="applications")
    op.drop_index("ix_applications_company", table_name="applications")
    op.drop_table("applications")
    application_status.drop(op.get_bind(), checkfirst=True)
