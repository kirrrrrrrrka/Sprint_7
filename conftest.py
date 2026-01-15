import pytest
import generators
from api.courier_api import CourierApi


@pytest.fixture
def create_and_delete_courier():
    """Фикстура для создания и удаления курьера"""
    courier_api = CourierApi()
    
    # Создаем курьера
    courier_data = generators.register_new_courier_and_return_login_password()
    
    if not courier_data:
        pytest.skip("Не удалось создать курьера")
    
    login, password, first_name = courier_data
    
    # Логинимся, чтобы получить ID
    login_response = courier_api.login_courier(login, password)
    courier_id = login_response.json().get("id") if login_response.status_code == 200 else None
    
    yield {
        "login": login,
        "password": password,
        "first_name": first_name,
        "id": courier_id
    }
    
    # Cleanup - удаление курьера (если в API есть такой метод)
    # Обычно в тестовых API нет метода удаления, поэтому пропускаем