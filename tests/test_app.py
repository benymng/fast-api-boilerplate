import importlib
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    import os

    os.environ["DATABASE_URL"] = "sqlite://"
    os.environ["ENVIRONMENT"] = "test"

    config = importlib.import_module("app.config")
    config.get_settings.cache_clear()
    main = importlib.import_module("app.main")

    with TestClient(main.app) as test_client:
        yield test_client


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_user_crud_flow(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/users",
        json={
            "email": "ada@example.com",
            "username": "ada",
            "password": "correct-horse-battery-staple",
        },
    )

    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["email"] == "ada@example.com"
    assert created_user["username"] == "ada"
    assert "password" not in created_user
    assert "hashed_password" not in created_user

    list_response = client.get("/api/v1/users")
    assert list_response.status_code == 200
    assert [user["email"] for user in list_response.json()] == ["ada@example.com"]

    update_response = client.patch(
        f"/api/v1/users/{created_user['id']}",
        json={"username": "ada-lovelace"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["username"] == "ada-lovelace"

    delete_response = client.delete(f"/api/v1/users/{created_user['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/users/{created_user['id']}")
    assert missing_response.status_code == 404
