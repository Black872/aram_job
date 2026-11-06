from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=255)
    role_title: str = Field(min_length=1, max_length=255)

    salary_rate: str | None = Field(default=None, max_length=100)
    job_advert_url: str | None = None
    application_date: date | None = None

    contact_name: str | None = Field(default=None, max_length=255)
    contact_email: str | None = Field(default=None, max_length=320)
    contact_phone: str | None = Field(default=None, max_length=80)

    response_status_raw: str | None = None
    interview_stage: str | None = Field(default=None, max_length=255)
    interview_at: datetime | None = None
    interviewer_name: str | None = Field(default=None, max_length=255)
    offer_status_raw: str | None = Field(default=None, max_length=100)

    status: ApplicationStatus = ApplicationStatus.APPLIED
    spreadsheet_tab: str | None = Field(default=None, max_length=255)
    spreadsheet_row_id: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=255)
    role_title: str | None = Field(default=None, min_length=1, max_length=255)

    salary_rate: str | None = Field(default=None, max_length=100)
    job_advert_url: str | None = None
    application_date: date | None = None

    contact_name: str | None = Field(default=None, max_length=255)
    contact_email: str | None = Field(default=None, max_length=320)
    contact_phone: str | None = Field(default=None, max_length=80)

    response_status_raw: str | None = None
    interview_stage: str | None = Field(default=None, max_length=255)
    interview_at: datetime | None = None
    interviewer_name: str | None = Field(default=None, max_length=255)
    offer_status_raw: str | None = Field(default=None, max_length=100)

    status: ApplicationStatus | None = None
    spreadsheet_tab: str | None = Field(default=None, max_length=255)
    spreadsheet_row_id: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role_title: str
    salary_rate: str | None
    job_advert_url: str | None
    application_date: date | None
    contact_name: str | None
    contact_email: str | None
    contact_phone: str | None
    response_status_raw: str | None
    interview_stage: str | None
    interview_at: datetime | None
    interviewer_name: str | None
    offer_status_raw: str | None
    status: ApplicationStatus
    spreadsheet_tab: str | None
    spreadsheet_row_id: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class ApplicationListResponse(BaseModel):
    items: list[ApplicationRead]
    total: int
    limit: int
    offset: int
