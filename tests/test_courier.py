import pytest
import allure
import generators
from api.courier_api import CourierApi
from data.test_data import TestData


class TestCourier:
    @allure.title("Тест: Успешное создание курьера")
    def test_create_courier_success(self):
        """Тест успешного создания курьера"""
        courier_api = CourierApi()
        login = generators.generate_random_string(10)
        password = generators.generate_random_string(10)
        first_name = generators.generate_random_string(10)
        
        response = courier_api.create_courier(login, password, first_name)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert response.json().get("ok") == True, "Ответ не содержит ok: true"
        
        # Получаем ID для очистки
        login_response = courier_api.login_courier(login, password)
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            courier_api.delete_courier(courier_id)

    @allure.title("Тест: Создание курьера с дублирующимся логином")
    def test_create_courier_duplicate_login(self, create_test_courier):
        """Тест создания курьера с уже существующим логином"""
        courier_api = CourierApi()
        
        # Пытаемся создать курьера с тем же логином
        response = courier_api.create_courier(
            create_test_courier["login"],
            "different_password",
            "different_name"
        )
        
        assert response.status_code == 409, f"Ожидался статус 409, получен {response.status_code}"
        error_message = response.json().get("message", "")
        assert "Этот логин уже используется" == error_message, f"Неверное сообщение об ошибке: {error_message}"

    @allure.title("Тест: Создание курьера без логина")
    def test_create_courier_missing_login(self):
        """Тест создания курьера без логина"""
        courier_api = CourierApi()
        
        response = courier_api.create_courier(
            "",  # Пустой логин
            "password123",
            "Test Name"
        )
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Тест: Создание курьера без пароля")
    def test_create_courier_missing_password(self):
        """Тест создания курьера без пароля"""
        courier_api = CourierApi()
        unique_login = f"test_{generators.generate_random_string(10)}"
        
        response = courier_api.create_courier(
            unique_login,
            "",  # Пустой пароль
            "Test Name"
        )
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Тест: Создание курьера без имени")
    def test_create_courier_missing_first_name(self):
        """Тест создания курьера без имени"""
        courier_api = CourierApi()
        unique_login = f"test_{generators.generate_random_string(10)}"
        
        response = courier_api.create_courier(
            unique_login,
            "password123",
            ""  # Пустое имя
        )
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Тест: Успешный логин курьера")
    def test_login_courier_success(self, create_test_courier):
        """Тест успешного логина курьера"""
        courier_api = CourierApi()
        
        response = courier_api.login_courier(
            create_test_courier["login"],
            create_test_courier["password"]
        )
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert "id" in response.json(), "Ответ не содержит ID курьера"

    @allure.title("Тест: Логин курьера без логина")
    def test_login_courier_missing_login(self):
        """Тест логина без логина"""
        courier_api = CourierApi()
        
        response = courier_api.login_courier("", "password123")
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Тест: Логин курьера без пароля")
    def test_login_courier_missing_password(self):
        """Тест логина без пароля"""
        courier_api = CourierApi()
        
        response = courier_api.login_courier("login123", "")
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Тест: Логин курьера с неверными учетными данными")
    def test_login_courier_invalid_credentials(self):
        """Тест логина с неверными учетными данными"""
        courier_api = CourierApi()
        
        response = courier_api.login_courier(
            "nonexistent_login",
            "wrong_password"
        )
        
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        assert response.json()["message"] == "Учетная запись не найдена"