import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture
def reset_activity_participants():
    original_participants = activities["Chess Club"]["participants"].copy()
    activities["Chess Club"]["participants"] = []
    yield
    activities["Chess Club"]["participants"] = original_participants


def test_unregister_existing_participant(reset_activity_participants):
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    activities[activity_name]["participants"].append(email)

    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert activities[activity_name]["participants"] == []


def test_unregister_missing_participant(reset_activity_participants):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not registered for this activity"
    }
