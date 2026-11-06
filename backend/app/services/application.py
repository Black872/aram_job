from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.application import Application, ApplicationStatus
from app.models.email_event import EmailEvent
from app.models.pending_action import PendingAction
from app.models.status_history import StatusHistory
from app.schemas.application import ApplicationCreate, ApplicationUpdate


def create_application(db: Session, data: ApplicationCreate) -> Application:
    application = Application(**data.model_dump())

    db.add(application)
    db.flush()

    db.add(
        StatusHistory(
            application_id=application.id,
            old_status=None,
            new_status=application.status.value,
            reason="Application created",
            source="MANUAL",
        )
    )

    db.commit()
    db.refresh(application)
    return application


def get_application(db: Session, application_id: int) -> Application | None:
    return db.get(Application, application_id)


def list_applications(
    db: Session,
    status: ApplicationStatus | None = None,
    company: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[Application], int]:
    query = select(Application)

    if status is not None:
        query = query.where(Application.status == status)

    if company:
        query = query.where(Application.company.ilike(f"%{company}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total = db.scalar(count_query) or 0

    query = (
        query.order_by(Application.created_at.desc(), Application.id.desc())
        .limit(limit)
        .offset(offset)
    )

    applications = list(db.scalars(query).all())
    return applications, total


def update_application(
    db: Session,
    application: Application,
    data: ApplicationUpdate,
) -> Application:
    updates = data.model_dump(exclude_unset=True)

    for field in ("company", "role_title", "status"):
        if field in updates and updates[field] is None:
            raise ValueError(f"{field} cannot be null")

    old_status = application.status

    for field, value in updates.items():
        setattr(application, field, value)

    if application.status != old_status:
        db.add(
            StatusHistory(
                application_id=application.id,
                old_status=old_status.value,
                new_status=application.status.value,
                reason="Status changed via API",
                source="MANUAL",
            )
        )

    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application: Application) -> None:
    has_email_events = db.scalar(
        select(EmailEvent.id)
        .where(EmailEvent.application_id == application.id)
        .limit(1)
    )

    has_pending_actions = db.scalar(
        select(PendingAction.id)
        .where(PendingAction.application_id == application.id)
        .limit(1)
    )

    if has_email_events or has_pending_actions:
        raise ValueError(
            "Application has linked email events or pending actions. "
            "Deletion is blocked to preserve related data."
        )

    db.query(StatusHistory).filter(
        StatusHistory.application_id == application.id
    ).delete(synchronize_session=False)

    db.delete(application)
    db.commit()
