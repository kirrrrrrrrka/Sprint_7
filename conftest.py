import pytest
import allure
import generators
from api.courier_api import CourierApi


@pytest.fixture
def create_test_courier():
    """Фикстура для создания тестового курьера"""
    courier_api = CourierApi()
    
    # Создаем курьера
    courier_data = generators.register_new_courier_and_return_login_password()
    
    if not courier_data:
        pytest.fail("Не удалось создать курьера для теста")
    
    login, password, first_name = courier_data
    
    # Логинимся, чтобы получить ID
    with allure.step(f"Логин курьера {login}"):
        login_response = courier_api.login_courier(login, password)
        assert login_response.status_code == 200, f"Не удалось залогиниться под курьером {login}"
        courier_id = login_response.json().get("id")
    
    yield {
        "login": login,
        "password": password,
        "first_name": first_name,
        "id": courier_id
    }
    
    # Очистка - удаление курьера
    with allure.step(f"Удаление курьера с ID {courier_id}"):
        if courier_id:
            delete_response = courier_api.delete_courier(courier_id)
            assert delete_response.status_code == 200, f"Не удалось удалить курьера {courier_id}"


@pytest.fixture
def create_test_courier_without_id():
    """Фикстура для создания тестового курьера без получения ID"""
    courier_api = CourierApi()
    
    # Создаем курьера
    courier_data = generators.register_new_courier_and_return_login_password()
    
    if not courier_data:
        pytest.fail("Не удалось создать курьера для теста")
    
    login, password, first_name = courier_data
    
    yield {
        "login": login,
        "password": password,
        "first_name": first_name
    }


@pytest.fixture
def get_courier_id(create_test_courier):
    """Фикстура для получения ID курьера"""
    return create_test_courier["id"]