class Storage:
    def __init__(self):
        super(Storage, self).__init__()
        self.__storage_name = None
        self.__storage_capacity = None
        self.__storage_price = 0

    # getters
    def get_info(self):
        return self.__storage_name

    def get_name(self):
        return self.__storage_name

    def get_storage_capacity(self):
        return "Storage capacity: " + self.__storage_capacity

    def get_price(self):
        return self.__storage_price

    # setters
    def set_name(self, name):
        self.__storage_name = name

    def set_storage_capacity(self, capacity):
        self.__storage_capacity = capacity


    def set_price(self, price):
        self.__storage_price = price
