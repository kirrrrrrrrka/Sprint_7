import requests


class BaseApi:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

    @staticmethod
    def get_headers():
        return {
            'Content-Type': 'application/json'
        }

    def get(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.get(url, params=params, headers=self.get_headers())

    def post(self, endpoint, data=None):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.post(url, json=data, headers=self.get_headers())

    def delete(self, endpoint, data=None):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.delete(url, json=data, headers=self.get_headers())