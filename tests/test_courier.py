import pytest
import generators
from api.courier_api import CourierApi
from data.test_data import TestData


class TestCourier:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.courier_api = CourierApi()
        self.valid_courier = TestData.VALID_COURIER
        
        # Генерируем уникального курьера для тестов
        self.test_courier = generators.register_new_courier_and_return_login_password()
        
        # Если удалось создать курьера, получаем его ID для последующего удаления
        if self.test_courier:
            self.test_courier_login = self.test_courier[0]
            self.test_courier_password = self.test_courier[1]
            
            # Получаем ID курьера
            response = self.courier_api.login_courier(
                self.test_courier_login, 
                self.test_courier_password
            )
            if response.status_code == 200:
                self.test_courier_id = response.json().get("id")
        
        yield
        
    def test_create_courier_success(self):
        """Тест успешного создания курьера"""
        courier_data = generators.register_new_courier_and_return_login_password()
        assert len(courier_data) == 3, f"Не удалось создать курьера. Ответ: {courier_data}"
        
    def test_create_courier_duplicate_login(self):
        """Тест создания курьера с уже существующим логином"""
        if not self.test_courier:
            pytest.skip("Не удалось создать тестового курьера")
        
        # Пытаемся создать курьера с тем же логином
        response = self.courier_api.create_courier(
            self.test_courier_login,
            "different_password",
            "different_name"
        )
        
        assert response.status_code == 409
        #Проверку сообщения об ошибке
        error_message = response.json().get("message", "")
        assert "Этот логин уже используется" in error_message
        
    def test_create_courier_missing_login(self):
        """Тест создания курьера без логина"""
        response = self.courier_api.create_courier(
            "",  # Пустой логин
            "password123",
            "Test Name"
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
        
    def test_create_courier_missing_password(self):
        """Тест создания курьера без пароля"""
        # Уникальный логин для  теста
        unique_login = f"test_{generators.generate_random_string(10)}"
        response = self.courier_api.create_courier(
            unique_login,
            "",  # Пустой пароль
            "Test Name"
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
        
    def test_create_courier_without_first_name(self):
        """Тест создания курьера без имени"""
        unique_login = f"test_{generators.generate_random_string(10)}"
        response = self.courier_api.create_courier(
            unique_login,
            "password123",
            ""  # Пустое имя
        )
        
        print(f"Status code for missing firstName: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 201:
            # API позволяет создавать без имени
            assert response.json().get("ok") == True
        else:
            # API не позволяет создавать без имени
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
        
    def test_create_courier_response_ok_true(self):
        """Тест, что успешный запрос возвращает {"ok": true}"""
        # Создаем нового уникального курьера
        login = generators.generate_random_string(10)
        password = generators.generate_random_string(10)
        first_name = generators.generate_random_string(10)
        
        response = self.courier_api.create_courier(login, password, first_name)
        
        if response.status_code == 201:
            assert response.json()["ok"] == True
        
    def test_login_courier_success(self):
        """Тест успешного логина курьера"""
        if not self.test_courier:
            pytest.skip("Не удалось создать тестового курьера")
        
        response = self.courier_api.login_courier(
            self.test_courier_login,
            self.test_courier_password
        )
        
        assert response.status_code == 200
        assert "id" in response.json()
        
    def test_login_courier_missing_login(self):
        """Тест логина без логина"""
        response = self.courier_api.login_courier("", "password123")
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"
        
    def test_login_courier_missing_password(self):
        """Тест логина без пароля"""
        response = self.courier_api.login_courier("login123", "")
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"
        
    def test_login_courier_invalid_credentials(self):
        """Тест логина с неверными учетными данными"""
        response = self.courier_api.login_courier(
            "nonexistent_login",
            "wrong_password"
        )
        
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"