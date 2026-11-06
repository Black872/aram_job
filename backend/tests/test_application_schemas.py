import pytest
from pydantic import ValidationError

from app.models.application import ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationUpdate


def test_application_create_defaults():
    application = ApplicationCreate(
        company="Example GmbH",
        role_title="Junior DevOps Engineer",
    )

    assert application.status == ApplicationStatus.APPLIED
    assert application.company == "Example GmbH"


def test_application_create_requires_company():
    with pytest.raises(ValidationError):
        ApplicationCreate(role_title="DevOps Engineer")


def test_application_update_only_contains_provided_fields():
    update = ApplicationUpdate(status=ApplicationStatus.INTERVIEW)

    assert update.model_dump(exclude_unset=True) == {
        "status": ApplicationStatus.INTERVIEW
    }
