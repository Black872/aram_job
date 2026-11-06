from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PendingAction(Base):
    __tablename__ = "pending_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int | None] = mapped_column(
        ForeignKey("applications.id", ondelete="SET NULL"), index=True
    )
    email_event_id: Mapped[int | None] = mapped_column(
        ForeignKey("email_events.id", ondelete="SET NULL"), index=True
    )
    action_type: Mapped[str] = mapped_column(String(80), nullable=False)
    proposed_changes: Mapped[dict] = mapped_column(JSON, nullable=False)
    confidence: Mapped[float | None]
    status: Mapped[str] = mapped_column(String(40), default="PENDING", nullable=False, index=True)
    review_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    application = relationship("Application", back_populates="pending_actions")
