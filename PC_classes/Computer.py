# from Case import Case
# from Motherboard import Motherboard
# from CPU import CPU
# from GPU import GPU
# from storage import Storage
# from cooling import Cooling
# from Case import Case
# from Power_Supply import power_supply
# from Wifi_card import wifi_card
# from Opsys import OpSys
# from Memory import Memory

class Computer:
    count_id = 0
    def __init__(self, case, motherboard, cpu, gpu, storage, cooling, power_supply, wifi, op_sys, memory):
        Computer.count_id += 1
        self.__id = Computer.count_id
        self.__description = None
        self.__case = case
        self.__motherboard = motherboard
        self.__cpu = cpu
        self.__gpu = gpu
        self.__storage = storage
        self.__cooling  = cooling
        self.__power_supply = power_supply
        self.__wifi = wifi
        self.__op_sys = op_sys
        self.__memory = memory


    def set_id(self, id):
        self.__id = id

    def set_description(self, description):
        self.__description = description

    def set_case(self, case):
        self.__case = case

    def set_motherboard(self, motherboard):
        self.__motherboard = motherboard

    def set_cpu(self, cpu):
        self.__cpu = cpu

    def set_gpu(self, gpu):
        self.__gpu = gpu

    def set_storage(self, storage):
        self.__storage = storage

    def set_cooling(self, cooling):
        self.__cooling = cooling

    def set_power_supply(self, power_supply):
        self.__power_supply = power_supply

    def set_wifi(self, wifi):
        self.__wifi = wifi

    def set_opsys(self, op_sys):
        self.__op_sys = op_sys

    def set_memory(self, memory):
        self.__memory = memory

    def get_info(self):
        return [f"{self.get_case().split(',')[1]}",
               f"{self.get_motherboard().split(',')[1]}",
               f"{self.get_cpu().split(',')[1]}",
               f"{self.get_gpu().split(',')[1]}",
               f"{self.get_storage().split(',')[1]}",
               f"{self.get_cooling().split(',')[1]}",
               f"{self.get_power_supply().split(',')[1]}",
               f"{self.get_wifi().split(',')[1]}",
               f"{self.get_opsys().split(',')[1]}",
               f"{self.get_memory().split(',')[1]}"]

    def get_id(self):
        return self.__id

    def get_description(self):
        return self.__description

    def get_case(self):
        return self.__case

    def get_motherboard(self):
        return self.__motherboard

    def get_cpu(self):
        return self.__cpu

    def get_gpu(self):
        return self.__gpu

    def get_storage(self):
        return self.__storage

    def get_cooling(self):
        return self.__cooling

    def get_power_supply(self):
        return self.__power_supply

    def get_wifi(self):
        return self.__wifi

    def get_opsys(self):
        return self.__op_sys

    def get_memory(self):
        return self.__memory

