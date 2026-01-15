class TestData:
    # Тестовые данные для курьера
    VALID_COURIER = {
        "login": "ninja",
        "password": "1234",
        "firstName": "saske"
    }
    
    COURIER_WITHOUT_LOGIN = {
        "password": "1234",
        "firstName": "saske"
    }
    
    COURIER_WITHOUT_PASSWORD = {
        "login": "ninja",
        "firstName": "saske"
    }
    
    COURIER_WITHOUT_FIRST_NAME = {
        "login": "ninja",
        "password": "1234"
    }
    
    # Тестовые данные для заказа
    ORDER_DATA = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-12-31",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]
    }
    
    ORDER_DATA_GREY = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-12-31",
        "comment": "Saske, come back to Konoha",
        "color": ["GREY"]
    }
    
    ORDER_DATA_BOTH_COLORS = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-12-31",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK", "GREY"]
    }
    
    ORDER_DATA_NO_COLOR = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-12-31",
        "comment": "Saske, come back to Konoha"
    }