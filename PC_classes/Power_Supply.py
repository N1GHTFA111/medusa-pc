class power_supply:
    def __init__(self):
        self.__name = None
        self.__price = 0

    def get_info(self):
        return self.__name

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price
