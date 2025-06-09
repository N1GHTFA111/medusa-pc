class Motherboard:
    def __init__(self):
        super(Motherboard, self).__init__()
        self.__model = None
        self.__price = 0

    def get_info(self):
        return self.__model

    def get_name(self):
        return self.__model

    def get_price(self):
        return self.__price

    def set_name(self,model):
        self.__model = model

    def set_price(self, price):
        self.__price = price
