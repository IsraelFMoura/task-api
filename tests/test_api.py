import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base, get_db
from main import app

# Banco de dados em memória, isolado para os testes.
# StaticPool garante que todas as conexões usem o mesmo banco em memória.
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def register_and_login(client, email="user@example.com", password="senha123"):
    client.post("/auth/register", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_user(client):
    response = client.post(
        "/auth/register", json={"email": "novo@example.com", "password": "senha123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "novo@example.com"


def test_register_duplicate_email_fails(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "senha123"})
    response = client.post(
        "/auth/register", json={"email": "dup@example.com", "password": "outrasenha"}
    )
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"email": "login@example.com", "password": "senha123"})
    response = client.post(
        "/auth/login", data={"username": "login@example.com", "password": "senha123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password_fails(client):
    client.post("/auth/register", json={"email": "wrong@example.com", "password": "senha123"})
    response = client.post(
        "/auth/login", data={"username": "wrong@example.com", "password": "errada"}
    )
    assert response.status_code == 401


def test_create_task_requires_auth(client):
    response = client.post("/tasks/", json={"title": "Sem auth"})
    assert response.status_code == 401


def test_create_and_list_tasks(client):
    headers = register_and_login(client)

    response = client.post(
        "/tasks/", json={"title": "Estudar FastAPI", "description": "Portfólio"}, headers=headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Estudar FastAPI"

    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_task(client):
    headers = register_and_login(client)
    create = client.post("/tasks/", json={"title": "Tarefa original"}, headers=headers)
    task_id = create.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}", json={"completed": True}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task(client):
    headers = register_and_login(client)
    create = client.post("/tasks/", json={"title": "Para deletar"}, headers=headers)
    task_id = create.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 404


def test_user_cannot_access_other_users_tasks(client):
    headers_a = register_and_login(client, email="usera@example.com")
    headers_b = register_and_login(client, email="userb@example.com")

    create = client.post("/tasks/", json={"title": "Tarefa da A"}, headers=headers_a)
    task_id = create.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=headers_b)
    assert response.status_code == 404
