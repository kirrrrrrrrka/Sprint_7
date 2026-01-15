import pytest
import generators
from api.order_api import OrderApi
from data.test_data import TestData


class TestOrder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.order_api = OrderApi()
        
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        """Параметризованный тест создания заказа с разными цветами"""
        order_data = generators.generate_order_data(color)
        response = self.order_api.create_order(order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()
        
    def test_create_order_black_color(self):
        """Тест создания заказа с черным цветом"""
        response = self.order_api.create_order(TestData.ORDER_DATA)
        
        assert response.status_code == 201
        assert "track" in response.json()
        
    def test_create_order_grey_color(self):
        """Тест создания заказа с серым цветом"""
        response = self.order_api.create_order(TestData.ORDER_DATA_GREY)
        
        assert response.status_code == 201
        assert "track" in response.json()
        
    def test_create_order_both_colors(self):
        """Тест создания заказа с обоими цветами"""
        response = self.order_api.create_order(TestData.ORDER_DATA_BOTH_COLORS)
        
        assert response.status_code == 201
        assert "track" in response.json()
        
    def test_create_order_no_color(self):
        """Тест создания заказа без указания цвета"""
        response = self.order_api.create_order(TestData.ORDER_DATA_NO_COLOR)
        
        assert response.status_code == 201
        assert "track" in response.json()