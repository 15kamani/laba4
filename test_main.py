# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# # Тестирование регистрации пользователя
# def test_register_user():
#     response = client.post(
#         "/register/",
#         json={
#             "username": "testuser",
#             "email": "testuser@example.com",
#             "full_name": "Test User",
#             "password": "password123"
#         },
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["username"] == "testuser"
#     assert data["email"] == "testuser@example.com"

# def test_register_user_duplicate():
#     response = client.post(
#         "/register/",
#         json={
#             "username": "testuser",
#             "email": "testuser@example.com",
#             "full_name": "Test User",
#             "password": "password123"
#         },
#     )
#     assert response.status_code == 400  # Предполагаем, что дубликат возвращает 400

# # Тестирование аутентификации
# def test_login_user():
#     response = client.post(
#         "/login/",
#         data={"username": "testuser", "password": "password123"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "access_token" in data
#     return data["access_token"]

# def test_login_user_invalid():
#     response = client.post(
#         "/login/",
#         data={"username": "testuser", "password": "wrongpassword"}
#     )
#     assert response.status_code == 401  # Предполагаем, что неверные данные возвращают 401

# def test_invalid_token():
#     response = client.get(
#         "/users/me",
#         headers={"Authorization": "Bearer invalid_token"}
#     )
#     assert response.status_code == 401  # Предполагаем, что неверный токен возвращает 401

# # Тестирование получения пользователей
# def test_get_users(token):
#     response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) > 0
#     assert data[0]["username"] == "testuser"
#     assert data[0]["email"] == "testuser@example.com"

# def test_get_current_user(token):
#     response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["username"] == "testuser"
#     assert data["email"] == "testuser@example.com"

# # Тестирование обновления пользователя
# def test_update_user(token):
#     response = client.put(
#         "/users/me",
#         headers={"Authorization": f"Bearer {token}"},
#         json={"full_name": "Updated Test User", "email": "updated@example.com"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["full_name"] == "Updated Test User"
#     assert data["email"] == "updated@example.com"

# def test_update_user_invalid(token):
#     response = client.put(
#         "/users/me",
#         headers={"Authorization": f"Bearer {token}"},
#         json={"full_name": "", "email": "invalid-email"}
#     )
#     assert response.status_code == 400  # Предполагаем, что некорректные данные возвращают 400

# def test_update_user_no_token():
#     response = client.put(
#         "/users/me",
#         json={"full_name": "Updated Test User", "email": "updated@example.com"}
#     )
#     assert response.status_code == 401  # Предполагаем, что отсутствие токена возвращает 401

# # Тестирование удаления пользователя
# def test_delete_user(token):
#     response = client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200

# def test_delete_user_again(token):
#     response = client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 404  # Предполагаем, что повторное удаление возвращает 404

# # Тестирование работы CORS
# def test_cors():
#     response = client.get("/", headers={"Origin": "http://allowed-origin.com"})
#     assert response.status_code == 200
#     assert "Access-Control-Allow-Origin" in response.headers
#     assert response.headers["Access-Control-Allow-Origin"] == "http://allowed-origin.com"

# def test_cors_disallowed():
#     response = client.get("/", headers={"Origin": "http://disallowed-origin.com"})
#     assert response.status_code == 400  # Предполагаем, что неподдерживаемый домен возвращает 400

# # Пример использования тестов
# if __name__ == "__main__":
#     token = test_login_user()
#     test_register_user()
#     test_register_user_duplicate()
#     test_login_user_invalid()
#     test_invalid_token()
#     test_get_users(token)
#     test_get_current_user(token)
#     test_update_user(token)
#     test_update_user_invalid(token)
#     test_update_user_no_token()
#     test_delete_user(token)
#     test_delete_user_again(token)
#     test_cors()
#     test_cors_disallowed()
