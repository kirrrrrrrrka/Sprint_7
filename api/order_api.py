from api.base_api import BaseApi


class OrderApi(BaseApi):
    def create_order(self, order_data):
        """Создание заказа"""
        return self.post("/orders", data=order_data)

    def get_order_list(self, courier_id=None, nearest_station=None, limit=30, page=0):
        """Получение списка заказов"""
        params = {}
        
        if courier_id is not None:
            params['courierId'] = courier_id
            
        if nearest_station is not None:
            params['nearestStation'] = nearest_station
            
        params['limit'] = limit
        params['page'] = page
        
        return self.get("/orders", params=params)

    def get_order_by_track(self, track):
        """Получение заказа по треку"""
        return self.get(f"/orders/track?t={track}")