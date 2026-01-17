import allure
from api.base_api import BaseApi


class CourierApi(BaseApi):
    @allure.step("Создание курьера с логином '{login}'")
    def create_courier(self, login, password, first_name):
        """Создание курьера"""
        data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return self.post("/courier", data=data)

    @allure.step("Логин курьера с логином '{login}'")
    def login_courier(self, login, password):
        """Логин курьера"""
        data = {
            "login": login,
            "password": password
        }
        return self.post("/courier/login", data=data)

    @allure.step("Удаление курьера с ID {courier_id}")
    def delete_courier(self, courier_id):
        """Удаление курьера"""
        return self.delete(f"/courier/{courier_id}")