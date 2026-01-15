import random
import string
import requests


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def register_new_courier_and_return_login_password():
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


def generate_order_data(color=None):
    """Генерация данных для заказа"""
    return {
        "firstName": generate_random_string(7),
        "lastName": generate_random_string(10),
        "address": f"Konoha, {random.randint(1, 200)} apt.",
        "metroStation": random.randint(1, 10),
        "phone": f"+7 800 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "comment": generate_random_string(20),
        "color": color if color else []
    }