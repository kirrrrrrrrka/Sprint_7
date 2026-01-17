import requests
import allure
from config import API_V1_URL


class BaseApi:
    BASE_URL = API_V1_URL

    @staticmethod
    def get_headers():
        return {
            'Content-Type': 'application/json'
        }

    @allure.step("GET запрос к {endpoint}")
    def get(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.get(url, params=params, headers=self.get_headers())

    @allure.step("POST запрос к {endpoint}")
    def post(self, endpoint, data=None):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.post(url, json=data, headers=self.get_headers())

    @allure.step("DELETE запрос к {endpoint}")
    def delete(self, endpoint, data=None):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.delete(url, json=data, headers=self.get_headers())