from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.application import ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationRead,
    ApplicationUpdate,
)
from app.services import application as service

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post(
    "",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
):
    return service.create_application(db, data)


@router.get("", response_model=ApplicationListResponse)
def list_applications(
    status_filter: ApplicationStatus | None = Query(default=None, alias="status"),
    company: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = service.list_applications(
        db=db,
        status=status_filter,
        company=company,
        limit=limit,
        offset=offset,
    )

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = service.get_application(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = service.get_application(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    try:
        return service.update_application(db, application, data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = service.get_application(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    try:
        service.delete_application(db, application)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
