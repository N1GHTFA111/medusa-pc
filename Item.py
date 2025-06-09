class Item:
    count_id = 0
    def __init__(self, item, description, price):
        Item.count_id += 1
        self._item = item
        self.__id = Item.count_id
        self.__description = description
        self.__price = price
        self.__collection_type = None
        self.__shipping_date = None
        self.__shipping_time = None
        self.__destination_address = None
        self.__owner = None

    def get_id(self):
        return self.__id

    def get_item(self):
        return self._item

    def get_price(self):
        return self.__price

    def get_description(self):
        return self.__description

    def get_collection_type(self):
        return self.__collection_type

    def get_shipping_date(self):
        return self.__shipping_date

    def get_shipping_time(self):
        return self.__shipping_time

    def get_destination_address(self):
        return self.__destination_address

    def get_owner(self):
        return self.__owner

    def set_id(self, id):
        self.__id = id

    def set_item(self, item):
        self._item = item

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    def set_collection_type(self, collection_type):
        self.__collection_type = collection_type

    def set_shipping_date(self, shipping_date):
        self.__shipping_date = shipping_date

    def set_shipping_time(self, shipping_time):
        self.__shipping_time = shipping_time

    def set_destination_address(self, destination_address):
        self.__destination_address = destination_address

    def set_owner(self, owner):
        self.__owner = owner
