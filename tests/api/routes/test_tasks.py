import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session
from src.core.config import settings
from tests.utils.tasks import create_random_task


def test_create_task(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_VERSION_STR}/tasks/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "user_id" in content


def test_read_task(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    task = create_random_task(db)
    response = client.get(
        f"{settings.API_VERSION_STR}/tasks/{task.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == task.title
    assert content["description"] == task.description
    assert content["id"] == str(task.id)
    assert content["user_id"] == str(task.user_id)


def test_read_task_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_VERSION_STR}/tasks/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Task not found"


def test_read_task_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    task = create_random_task(db)
    response = client.get(
        f"{settings.API_VERSION_STR}/tasks/{task.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not your task"


def test_read_tasks(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_task(db)
    create_random_task(db)
    response = client.get(
        f"{settings.API_VERSION_STR}/tasks/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["tasks"]) >= 2


def test_update_task(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    task = create_random_task(db)
    data = {"title": "Updated title", "status": "completed", "description": "Updated description"}
    response = client.put(
        f"{settings.API_VERSION_STR}/tasks/{task.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["status"] == data["status"]
    assert content["id"] == str(task.id)
    assert content["user_id"] == str(task.user_id)


def test_update_task_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_VERSION_STR}/tasks/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Task not found"


def test_update_task_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    task = create_random_task(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_VERSION_STR}/tasks/{task.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not your task"


def test_delete_task(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    task = create_random_task(db)
    response = client.delete(
        f"{settings.API_VERSION_STR}/tasks/{task.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Task deleted"


def test_delete_task_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_VERSION_STR}/tasks/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Task not found"


def test_delete_task_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    task = create_random_task(db)
    response = client.delete(
        f"{settings.API_VERSION_STR}/tasks/{task.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not your task"
