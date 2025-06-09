class CPU:
    def __init__(self):
        super(CPU, self).__init__()
        self.__cpu_name = None
        self.__cpu_price = 0
        self.__num_of_cores = 0
        self.__total_threads = 0
        self.__base_performance_freq = 0
        self.__max_performance_freq = 0
        self.__base_power = 0
        self.__max_power = 0


    # getters
    def get_info(self):
        return self.__cpu_name

    def get_name(self):
        return self.__cpu_name

    def get_price(self):
        return self.__cpu_price

    def get_cores_threads(self):
        return "Cores: " + str(self.__num_of_cores) + "\n" + "Threads: " + str(self.__total_threads)

    def get_performance_freq(self):
        return "Performance frequency: " + str(self.__base_performance_freq) + "-" + str(self.__max_performance_freq)

    def get_cpu_power_range(self):
        return "Power needed: " + str(self.__base_power) + "-" + str(self.__max_power) + "W"

    # setters
    def set_name(self, cpu_name):
        self.__cpu_name = cpu_name

    def set_price(self, cpu_price):
        self.__cpu_price = cpu_price

    def set_cores_threads(self, num_cores, num_threads):
        self.__num_of_cores = num_cores
        self.__total_threads = num_threads

    def set_performance_freq(self, min_freq, max_freq):
        self.__base_performance_freq = min_freq
        self.__max_performance_freq = max_freq

    def set_cpu_power_range(self, base_pow, max_pow):
        self.__base_power = base_pow
        self.__max_power = max_pow
