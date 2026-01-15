import pytest
import generators
from api.order_api import OrderApi
from api.courier_api import CourierApi


class TestOrderList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.order_api = OrderApi()
        self.courier_api = CourierApi()
        
        # Создаем тестового курьера
        self.test_courier = generators.register_new_courier_and_return_login_password()
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
        
    def test_get_order_list_without_params(self):
        """Тест получения списка заказов без параметров"""
        response = self.order_api.get_order_list()
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
        
    def test_get_order_list_with_limit(self):
        """Тест получения списка заказов с лимитом"""
        response = self.order_api.get_order_list(limit=5)
        
        assert response.status_code == 200
        orders = response.json()["orders"]
        assert len(orders) <= 5
        
    def test_get_order_list_with_page(self):
        """Тест получения списка заказов с указанием страницы"""
        response = self.order_api.get_order_list(page=0, limit=5)
        
        assert response.status_code == 200
        orders = response.json()["orders"]
        assert isinstance(orders, list)
        
    def test_get_order_list_with_nonexistent_courier(self):
        """Тест получения списка заказов с несуществующим courierId"""
        nonexistent_id = 999999
        
        response = self.order_api.get_order_list(courier_id=nonexistent_id)
        
        assert response.status_code == 404
        assert response.json()["message"] == f"Курьер с идентификатором {nonexistent_id} не найден"