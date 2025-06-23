from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal

client = TestClient(app)

def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_and_get_user():
    response = client.post("/users/", json={
        "name": "Alice",
        "email": "alice@example.com",
        "skills_offered": ["Python"],
        "skills_needed": ["React"]
    })
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]

    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "alice@example.com"
