# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SkillSwap API!"}

def test_create_user():
    response = client.post("/users/", json={
        "name": "Alice",
        "email": "alice@example.com",
        "skills_offered": ["Python"],
        "skills_needed": ["React"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"

def test_get_user():
    user = client.post("/users/", json={
        "name": "Bob",
        "email": "bob@example.com",
        "skills_offered": ["JavaScript"],
        "skills_needed": ["Go"]
    })
    user_id = user.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Bob"

def test_update_user():
    user = client.post("/users/", json={
        "name": "Charlie",
        "email": "charlie@example.com",
        "skills_offered": ["C++"],
        "skills_needed": ["Rust"]
    })
    user_id = user.json()["id"]

    updated = client.put(f"/users/{user_id}", json={
        "name": "Charlie Updated",
        "email": "charlie@example.com",
        "skills_offered": ["Java"],
        "skills_needed": ["Go"]
    })
    assert updated.status_code == 200
    assert updated.json()["name"] == "Charlie Updated"

def test_delete_user():
    user = client.post("/users/", json={
        "name": "DeleteMe",
        "email": "deleteme@example.com",
        "skills_offered": ["Django"],
        "skills_needed": ["Flask"]
    })
    user_id = user.json()["id"]

    deleted = client.delete(f"/users/{user_id}")
    assert deleted.status_code == 200
    assert deleted.json()["message"] == "User deleted"

    check = client.get(f"/users/{user_id}")
    assert check.status_code == 404

def test_match_users():
    u1 = client.post("/users/", json={
        "name": "Match1",
        "email": "m1@example.com",
        "skills_offered": ["Java"],
        "skills_needed": ["C"]
    })
    u2 = client.post("/users/", json={
        "name": "Match2",
        "email": "m2@example.com",
        "skills_offered": ["C"],
        "skills_needed": ["Java"]
    })
    uid = u1.json()["id"]

    match = client.post("/match/", json={"user_id": uid})
    assert match.status_code == 200
    assert any(u["name"] == "Match2" for u in match.json())

def test_exchange_skills():
    sender = client.post("/users/", json={
        "name": "Sender",
        "email": "sender@example.com",
        "skills_offered": ["Angular"],
        "skills_needed": ["Flutter"]
    })
    receiver = client.post("/users/", json={
        "name": "Receiver",
        "email": "receiver@example.com",
        "skills_offered": ["Flutter"],
        "skills_needed": ["Angular"]
    })

    s_id = sender.json()["id"]
    r_id = receiver.json()["id"]

    response = client.post("/exchange/", json={
        "sender_id": s_id,
        "receiver_id": r_id,
        "skill_offered": "Angular",
        "skill_received": "Flutter"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["skill_offered"] == "Angular"
    assert data["sender_id"] == s_id
    assert data["receiver_id"] == r_id
    assert "timestamp" in data

def test_get_all_exchanges():
    response = client.get("/exchanges/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_match_ui():
    response = client.get("/match_ui")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
