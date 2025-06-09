class Case:
    def __init__(self):
        super(Case, self).__init__()
        self.__case_model = None
        self.__size_type = None
        self.__case_color = None
        self.__case_material = None

        self.__case_name = None
        self.__case_price = 0

    def get_info(self):
        return self.__case_name

    # getters
    def get_model(self):
        return self.__case_model

    def get_case_size_type(self):
        return "Case Size Type: " + self.__size_type

    def get_case_color(self):
        return "Case Color: " + self.__case_color

    def get_case_materials(self):
        return "Case Materials: " + self.__case_material

    def get_price(self):
        return self.__case_price

    # setters
    def set_name(self, case_name):
        self.__case_name = case_name

    def set_case_size_(self, size_type):
        self.__size_type = size_type

    def set_case_color(self, case_color):
        self.__case_color = case_color

    def set_case_materials(self, case_material):
        self.__case_material = case_material

    def set_price(self, price):
        self.__case_price = price

    def set_model(self, case_model):
        self.__case_model = case_model
