from fastapi.testclient import TestClient
import copy
import app as app_module

client = TestClient(app_module.app)

def setup_function():
    global _backup
    _backup = copy.deepcopy(app_module.activities)

def teardown_function():
    app_module.activities.clear()
    app_module.activities.update(_backup)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data

def test_signup_and_duplicate():
    activity = "Chess Club"
    email = "tester@example.com"
    assert email not in app_module.activities[activity]["participants"]
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 400

def test_unregister():
    activity = "Chess Club"
    email = "unreg@example.com"
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    resp2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 200
    assert email not in app_module.activities[activity]["participants"]

def test_unregister_not_signed_up_returns_400():
    activity = "Chess Club"
    email = "notthere@example.com"
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400
