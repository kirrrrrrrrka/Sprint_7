from api.base_api import BaseApi


class CourierApi(BaseApi):
    def create_courier(self, login, password, first_name):
        """Создание курьера"""
        data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return self.post("/courier", data=data)

    def login_courier(self, login, password):
        """Логин курьера"""
        data = {
            "login": login,
            "password": password
        }
        return self.post("/courier/login", data=data)

    def delete_courier(self, courier_id):
        """Удаление курьера (если такой метод существует в API)"""
        return self.delete(f"/courier/{courier_id}")