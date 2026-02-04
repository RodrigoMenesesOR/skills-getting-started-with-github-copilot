from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_contains_keys():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    activity_name = "Basketball"
    email = "pytest-user@example.com"

    # Ensure clean state
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity_name}"

    # Ensure participant appears in GET
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    assert email in resp2.json()[activity_name]["participants"]

    # Unregister
    resp3 = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert resp3.status_code == 200
    assert resp3.json()["message"] == f"Unregistered {email} from {activity_name}"

    # Ensure removed
    resp4 = client.get("/activities")
    assert email not in resp4.json()[activity_name]["participants"]


def test_unregister_nonexistent():
    activity_name = "Chess Club"
    email = "not-registered@example.com"

    # Ensure not registered
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Attempt to unregister should 404
    resp = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert resp.status_code == 404

