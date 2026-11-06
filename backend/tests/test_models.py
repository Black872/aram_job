from app.models.application import ApplicationStatus


def test_application_status_values():
    assert ApplicationStatus.APPLIED.value == "APPLIED"
    assert ApplicationStatus.REJECTED.value == "REJECTED"
    assert ApplicationStatus.OFFER.value == "OFFER"
