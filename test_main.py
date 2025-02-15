from fastapi.testclient import TestClient
from main import app  # Импортируем экземпляр FastAPI приложения из main.py

# Создаем экземпляр TestClient, передавая ему наше приложение
client = TestClient(app)

# Тест для проверки главной страницы
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

# Тест для получения списка пользователей
def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["username"] == "string"

# Тест для создания нового пользователя
def test_create_user():
    response = client.post(
        "/register/",
        json={"username": "testuser", "email": "testuser@example.com", "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"




# Тестирование регистрации пользователя
def test_register_user():
    # Успешная регистрация нового пользователя
    response = client.post(
        "/register/",
        json={"username": "testuser", "email": "testuser@example.com", "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

    # Попытка повторной регистрации с тем же username
    response = client.post(
        "/register/",
        json={"username": "testuser", "email": "another@example.com", "full_name": "Another User", "password": "password123"},
    )
    assert response.status_code == 400
    assert "username already registered" in response.json()["detail"]

    # Попытка повторной регистрации с тем же email
    response = client.post(
        "/register/",
        json={"username": "anotheruser", "email": "testuser@example.com", "full_name": "Another User", "password": "password123"},
    )
    assert response.status_code == 400
    assert "email already registered" in response.json()["detail"]


# Тестирование аутентификации
def test_authenticate_user():
    # Успешная аутентификация
    response = client.post(
        "/login/",
        data={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Неправильный username
    response = client.post(
        "/login/",
        data={"username": "wronguser", "password": "password123"},
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

    # Неправильный пароль
    response = client.post(
        "/login/",
        data={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

    # Проверка истёкшего или неправильного токена
    expired_token = "expired_token_here"
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


# Тестирование получения пользователей
def test_get_users():
    # Получение списка пользователей
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["username"] == "testuser"
    assert data[0]["email"] == "testuser@example.com"

    # Получение информации о текущем пользователе
    token_response = client.post(
        "/login/",
        data={"username": "testuser", "password": "password123"},
    )
    token = token_response.json()["access_token"]
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"


# Тестирование обновления пользователя
def test_update_user():
    # Успешное обновление данных пользователя
    token_response = client.post(
        "/login/",
        data={"username": "testuser", "password": "password123"},
    )
    token = token_response.json()["access_token"]
    response = client.put(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Updated Name", "email": "updated@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["email"] == "updated@example.com"

    # Обновление с некорректными данными
    response = client.put(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "invalid-email"},
    )
    assert response.status_code == 422

    # Обновление без токена
    response = client.put(
        "/users/me/",
        json={"full_name": "Unauthorized Update"},
    )
    assert response.status_code == 401



# Тестирование удаления пользователя
def test_delete_user():
    # Успешное удаление пользователя
    token_response = client.post(
        "/login/",
        data={"username": "testuser", "password": "password123"},
    )
    token = token_response.json()["access_token"]
    response = client.delete(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Повторная попытка удалить пользователя
    response = client.delete(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404



# Тестирование работы CORS
def test_cors():
    # Проверка CORS для поддерживаемого домена
    response = client.options(
        "/users/",
        headers={"Origin": "https://allowed-domain.com"},
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

    # Проверка CORS для неподдерживаемого домена
    response = client.options(
        "/users/",
        headers={"Origin": "https://disallowed-domain.com"},
    )
    assert response.status_code == 400



# Дополнительные задания
 
# Тестирование обработки ошибок
def test_error_handling():
    # Некорректные данные при регистрации
    response = client.post(
        "/register/",
        json={"username": "testuser"},  # Отсутствует обязательное поле email
    )
    assert response.status_code == 422

# Тестирование производительности
import time

def test_performance():
    start_time = time.time()
    for _ in range(100):  # 100 запросов
        client.get("/users/")
    end_time = time.time()
    assert end_time - start_time < 5  # Ожидаемое время выполнения

# Тестирование безопасности
def test_security():
    # Защищённый маршрут без токена
    response = client.get("/users/me/")
    assert response.status_code == 401

    # Защищённый маршрут с поддельным токеном
    response = client.get(
        "/users/me/",
        headers={"Authorization": "Bearer fake_token"},
    )
    assert response.status_code == 401