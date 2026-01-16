import pytest
import allure
from api.order_api import OrderApi


class TestOrderList:
    @allure.title("Тест: Получение списка заказов без параметров")
    def test_get_order_list_without_params(self):
        """Тест получения списка заказов без параметров"""
        order_api = OrderApi()
        response = order_api.get_order_list()
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert "orders" in response.json(), "Ответ не содержит ключ 'orders'"
        assert isinstance(response.json()["orders"], list), "Orders не является списком"

    @allure.title("Тест: Получение списка заказов с лимитом")
    def test_get_order_list_with_limit(self):
        """Тест получения списка заказов с лимитом"""
        order_api = OrderApi()
        response = order_api.get_order_list(limit=5)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        orders = response.json().get("orders", [])
        assert len(orders) <= 5, f"Получено {len(orders)} заказов, ожидалось не более 5"

    @allure.title("Тест: Получение списка заказов с указанием страницы")
    def test_get_order_list_with_page(self):
        """Тест получения списка заказов с указанием страницы"""
        order_api = OrderApi()
        response = order_api.get_order_list(page=0, limit=5)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        orders = response.json().get("orders", [])
        assert isinstance(orders, list), "Orders не является списком"

    @allure.title("Тест: Получение списка заказов с несуществующим courierId")
    def test_get_order_list_with_nonexistent_courier(self):
        """Тест получения списка заказов с несуществующим courierId"""
        order_api = OrderApi()
        nonexistent_id = 999999
        
        response = order_api.get_order_list(courier_id=nonexistent_id)
        
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        assert response.json()["message"] == f"Курьер с идентификатором {nonexistent_id} не найден"