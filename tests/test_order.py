import pytest
import allure
import generators
from api.order_api import OrderApi
from api.courier_api import CourierApi


class TestOrder:
    @allure.title("Тест: Создание заказа с разными цветами")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        """Параметризованный тест создания заказа с разными цветами"""
        order_api = OrderApi()
        courier_api = CourierApi()
        order_data = generators.generate_order_data(color)
        
        response = order_api.create_order(order_data)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response.json(), "Ответ не содержит track"
        
        # Получаем ID заказа для очистки (если в API есть метод удаления заказа)
        track = response.json().get("track")
        if track:
            order_response = order_api.get_order_by_track(track)
            if order_response.status_code == 200:
                order_id = order_response.json().get("order", {}).get("id")
                # Здесь можно добавить удаление заказа если API поддерживает

    @allure.title("Тест: Создание заказа с черным цветом")
    def test_create_order_black_color(self):
        """Тест создания заказа с черным цветом"""
        order_api = OrderApi()
        order_data = generators.generate_order_data(["BLACK"])
        
        response = order_api.create_order(order_data)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response.json(), "Ответ не содержит track"

    @allure.title("Тест: Создание заказа с серым цветом")
    def test_create_order_grey_color(self):
        """Тест создания заказа с серым цветом"""
        order_api = OrderApi()
        order_data = generators.generate_order_data(["GREY"])
        
        response = order_api.create_order(order_data)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response.json(), "Ответ не содержит track"

    @allure.title("Тест: Создание заказа с обоими цветами")
    def test_create_order_both_colors(self):
        """Тест создания заказа с обоими цветами"""
        order_api = OrderApi()
        order_data = generators.generate_order_data(["BLACK", "GREY"])
        
        response = order_api.create_order(order_data)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response.json(), "Ответ не содержит track"

    @allure.title("Тест: Создание заказа без указания цвета")
    def test_create_order_no_color(self):
        """Тест создания заказа без указания цвета"""
        order_api = OrderApi()
        order_data = generators.generate_order_data()
        
        response = order_api.create_order(order_data)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response.json(), "Ответ не содержит track"

    @allure.title("Тест: Получение заказа по трек номеру")
    def test_get_order_by_track(self):
        """Тест получения заказа по трек номеру"""
        order_api = OrderApi()
        order_data = generators.generate_order_data(["BLACK"])
        
        # Создаем тестовый заказ
        response = order_api.create_order(order_data)
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        track = response.json().get("track")
        assert track is not None, "Track не найден в ответе"
        
        # Получаем заказ по track
        track_response = order_api.get_order_by_track(track)
        assert track_response.status_code == 200, f"Ожидался статус 200, получен {track_response.status_code}"
        order_info = track_response.json().get("order")
        assert order_info is not None, "Информация о заказе не найдена"
        assert order_info.get("firstName") == order_data["firstName"], "Имя заказчика не совпадает"