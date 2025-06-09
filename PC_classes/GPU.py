class GPU:
    def __init__(self):
        super(GPU, self).__init__()
        self.__gpu_name = None
        self.__base_clock = None
        self.__boost_clock = None
        self.__power_needed = 0
        self.__gpu_price = 0

    # getters
    def get_info(self):
        return self.__gpu_name

    def get_name(self):
        return self.__gpu_name

    def get_gpu_speed(self):
        return "GPU Speed: " + self.__base_clock + "-" + self.__boost_clock + "MHz"

    def get_power_needed_gpu(self):
        return "Power needed for GPU: " + str(self.__power_needed)

    def get_price(self):
        return self.__gpu_price

    # setters
    def set_name(self, name):
        self.__gpu_name = name

    def set_gpu_speed(self, base_clock, boost_clock):
        self.__base_clock = base_clock
        self.__boost_clock = boost_clock

    def set_power_needed_gpu(self, power_needed):
        self.__power_needed = power_needed

    def set_price(self, gpu_price):
        self.__gpu_price = gpu_price
