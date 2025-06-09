

class Shipment:

    shipping_statuses = ["Pending", "In Progress", "Received"]

    def __init__(self):
        self.__shipping_id = None
        self.__item_to_ship = None
        self.__shipping_status = None
        self.__order_date = None

    def set_id(self, shipping_id):
        self.__shipping_id = shipping_id

    def set_item(self, item):
        self.__item_to_ship = item

    def set_shipping_status(self, shipping_status):
        if shipping_status in self.shipping_statuses:
            self.__shipping_status = shipping_status
        else:
            pass

    def set_order_date(self, order_date):
        self.__order_date = order_date

    def get_id(self):
        return self.__shipping_id

    def get_item(self):
        return self.__item_to_ship

    def get_shipping_status(self):
        return self.__shipping_status

    def get_order_date(self):
        return self.__order_date
