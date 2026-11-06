import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    RECEIVED = "RECEIVED"
    IN_REVIEW = "IN_REVIEW"
    INTERVIEW = "INTERVIEW"
    TECHNICAL_TEST = "TECHNICAL_TEST"
    REJECTED = "REJECTED"
    OFFER = "OFFER"
    WITHDRAWN = "WITHDRAWN"
    CLOSED = "CLOSED"
    UNKNOWN = "UNKNOWN"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    salary_rate: Mapped[str | None] = mapped_column(String(100))
    job_advert_url: Mapped[str | None] = mapped_column(Text)
    application_date: Mapped[date | None] = mapped_column(Date)
    contact_name: Mapped[str | None] = mapped_column(String(255))
    contact_email: Mapped[str | None] = mapped_column(String(320))
    contact_phone: Mapped[str | None] = mapped_column(String(80))
    response_status_raw: Mapped[str | None] = mapped_column(Text)
    interview_stage: Mapped[str | None] = mapped_column(String(255))
    interview_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    interviewer_name: Mapped[str | None] = mapped_column(String(255))
    offer_status_raw: Mapped[str | None] = mapped_column(String(100))

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"),
        default=ApplicationStatus.APPLIED,
        nullable=False,
        index=True,
    )
    spreadsheet_tab: Mapped[str | None] = mapped_column(String(255))
    spreadsheet_row_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now(), nullable=False
    )

    email_events = relationship("EmailEvent", back_populates="application")
    status_history = relationship("StatusHistory", back_populates="application")
    pending_actions = relationship("PendingAction", back_populates="application")
