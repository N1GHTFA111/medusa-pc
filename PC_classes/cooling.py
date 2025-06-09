class Cooling:
    def __init__(self):
        super(Cooling, self).__init__()
        self.__cooling_name = None
        self.__cooling_price = 0
        self.__cooling_type = None

    # getters
    def get_info(self):
        return self.__cooling_name

    def get_name(self):
        return self.__cooling_name

    def get_price(self):
        return self.__cooling_price

    def get_cooling_type(self):
        return "Cooling type: " + self.__cooling_type + " cooling"

    # setters

    def set_name(self, name):
        self.__cooling_name = name

    def set_price(self, price):
        self.__cooling_price = price

    def set_cooling_type(self, type):
        self.__cooling_type = type

