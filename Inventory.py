import shelve

class Inventory:
    def __init__(self):
        self.__cases = [("79,CM MB600L V2 Fan x1", 'CM MB600L V2 Fan x1'), ("140,Corsair 4000D Airflow", 'Corsair 4000D Airflow'), ("279,CM Mastercase H500M w_TG_U3_ARGB Fan x2", 'CM Mastercase H500M w_TG_U3_ARGB Fan x2'), ]
        self.__available_cases = []
        self.__cases_stock = []

        self.__cpu = [("290,Intel i5-12400", "Intel i5-12400"), ("599,Intel i7-12700", "Intel i7-12700"), ('617,Intel i7-13700k', 'Intel i7-13700k')]
        self.__available_cpu = []
        self.__cpu_stock = []

        self.__motherboards = [("379,Asus Prime Z790M-Plus D4-CSM", "Asus Prime Z790M-Plus D4-CSM"), ('535,Asus Tuf Gaming Z790-Plus wifi D4', 'Asus Tuf Gaming Z790-Plus wifi D4'), ('1129,Asus ROG Maximus Z790 Hero', 'Asus ROG Maximus Z790 Hero'),]
        self.__available_motherboards = []
        self.__motherboards_stock = []

        self.__cooling = [("39,ID-Cooling SE-224-XT Black V2 Fan x1", "ID-Cooling SE-224-XT Black V2 Fan x1"), ('159,Asus TUF Gaming LC240 ARGB', 'Asus TUF Gaming LC240 ARGB'), ('165,CoolerMaster MasterLiquid ML360L V2 A-RGB', 'CoolerMaster MasterLiquid ML360L V2 A-RGB')]
        self.__available_cooling = []
        self.__cooling_stock = []

        self.__memory = [("109,Corsair Vengeance LPX 3200 CL16 Intel-AMD 16GB", "Corsair Vengeance LPX 3200 CL16 Intel-AMD 16GB"), ('155,GSkill RipJaw V 3200 CL16 RGB 32GB', 'GSkill RipJaw V 3200 CL16 RGB 32GB'), ('390,GSkill Trident Z NEO 3200 CL16 Dual 64GB', 'GSkill Trident Z NEO 3200 CL16 Dual 64GB')]
        self.__available_memory = []
        self.__memory_stock = []

        self.__gpu = [("269,Asus TUF Gaming GTX1650 OC 4GB", "Asus TUF Gaming GTX1650 OC 4GB"), ('747,Asus TUF Gaming RTX3060Ti 8GB OC V2 GDDR6', 'Asus TUF Gaming RTX3060Ti 8GB OC V2 GDDR6'), ('1096,Asus TUF Gaming RTX3080 10GB OC V2 GDDR6X', 'Asus TUF Gaming RTX3080 10GB OC V2 GDDR6X')]
        self.__available_gpu = []
        self.__gpu_stock = []

        self.__primary_storage = [("199,Samsung 980 Pro 1TB", "Samsung 980 Pro 1TB"), ("249,Samsung 990 Pro 1TB", "Samsung 990 Pro 1TB"), ("399,Samsung 980 Pro 2TB", "Samsung 980 Pro 2TB"), ("489,Samsung 990 Pro 2TB", "Samsung 990 Pro 2TB"),]
        self.__available_storage = []
        self.__storage_stock = []

        self.__power_supply = [("129,Asus TUF Gaming 750W 80+Bronze", 'Asus TUF Gaming 750W 80+Bronze'), ('156,SilverStone DA850 850W 80-Plus Gold', 'SilverStone DA850 850W 80-Plus Gold'), ('365,Corsair HX1000i 80-Plus Platinum Modular', 'Corsair HX1000i 80-Plus Platinum Modular')]
        self.__available_power = []
        self.__power_stock = []

        self.__opsys= [("100,Windows 11 Home 64 bit", "Windows 11 Home 64 bit"), ('180', 'Windows 11 Pro 64 bit')]
        self.__available_opsys = []
        self.__opsys_stock = []

        self.__keyboards = [("101,CoolerMaster CK530 (Blue/Red)", "CoolerMaster CK530 (Blue/Red)"), ("139,MSI GK50 Elite Gaming Keyboard", "MSI GK50 Elite Gaming Keyboard"), ("269,Asus ROG Strix Scope (Red/Blue)", "Asus ROG Strix Scope (Red/Blue)")]
        self.__available_keyboards = []
        self.__keyboard_stock = []

        self.__mouse = [("19,Armageddon Scorpion 3", "Armageddon Scorpion 3"), ("55,Corsair M55 RGB Pro", "Corsair M55 RGB Pro"), ("129,Logitech G502 Hero","Logitech G502 Hero"), ("25,Razer Sphex V2 Mousepad", "Razer Sphex V2 Mousepad"), ("59,Corsair MM350 Pro Premium Mousepad", "Corsair MM350 Pro Premium Mousepad"), ("79,Razer RZ02 Mousepad RGB","Razer RZ02 Mousepad RGB")]
        self.__available_mouse = []
        self.__mouse_stock = []


    def replace_space_with_underscore(self, string):
        return string.replace(' ', '_')

    def update_products(self):
        products_dict = {}
        products_db = shelve.open('products.db', 'r')

        try:
            products_dict = products_db["PRODUCTS"]
        except:
            print("Error in retrieving products from products.db")

        self.__cases = []
        self.__cpu = []
        self.__motherboards = []
        self.__cooling = []
        self.__memory = []
        self.__gpu = []
        self.__primary_storage = []
        self.__power_supply = []
        self.__opsys = []
        self.__keyboards = []
        self.__mouse = []

        for case in products_dict["CASES"]:
            self.__cases.append(case)
        for cpu in products_dict["CPU"]:
            self.__cpu.append(cpu)
        for motherboard in products_dict["MOTHERBOARDS"]:
            self.__motherboards.append(motherboard)
        for cooling in products_dict["COOLING"]:
            self.__cooling.append(cooling)
        for memory in products_dict["MEMORY"]:
            self.__memory.append(memory)
        for gpu in products_dict["GPU"]:
            self.__gpu.append(gpu)
        for storage in products_dict["STORAGE"]:
            self.__primary_storage.append(storage)
        for power in products_dict["POWER"]:
            self.__power_supply.append(power)
        for opsys in products_dict["OPSYS"]:
            self.__opsys.append(opsys)
        for keyboard in products_dict["KEYBOARDS"]:
            self.__keyboards.append(keyboard)
        for mouse in products_dict["MOUSE"]:
            self.__mouse.append(mouse)



        products_db.close()

    # create the products.db to update the hardcoded products
    def gather_products(self):
        products_dict = {}
        products_db = shelve.open('products.db', 'c')

        try:
            products_dict = products_db["PRODUCTS"]
        except:
            print("Error in retrieving products from products.db")

        # retrieve the hard coded objects

        products_dict["CASES"] = []
        products_dict["CPU"] = []
        products_dict["MOTHERBOARDS"] = []
        products_dict["COOLING"] = []
        products_dict["MEMORY"] = []
        products_dict["GPU"] = []
        products_dict["STORAGE"] = []
        products_dict["POWER"] = []
        products_dict["OPSYS"] = []
        products_dict["KEYBOARDS"] = []
        products_dict["MOUSE"] = []

        for case in self.__cases:
            products_dict["CASES"].append(case)
        for cpu in self.__cpu:
            products_dict["CPU"].append(cpu)
        for motherboard in self.__motherboards:
            products_dict["MOTHERBOARDS"].append(motherboard)
        for cooling in self.__cooling:
            products_dict["COOLING"].append(cooling)
        for memory in self.__memory:
            products_dict["MEMORY"].append(memory)
        for gpu in self.__gpu:
            products_dict["GPU"].append(gpu)
        for storage in self.__primary_storage:
            products_dict["STORAGE"].append(storage)
        for power in self.__power_supply:
            products_dict["POWER"].append(power)
        for opsys in self.__opsys:
            products_dict["OPSYS"].append(opsys)
        for keyboard in self.__keyboards:
            products_dict["KEYBOARDS"].append(keyboard)
        for mouse in self.__mouse:
            products_dict["MOUSE"].append(mouse)

        products_db["PRODUCTS"] = products_dict

        products_db.close()

    def create_inventory(self):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'c')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        #need to add key/value pairs to inventory for cases
        inventory_cases_dict = {}
        null_case = []
        for case in self.__cases:
            inventory_cases_dict[case[1]] = 10
            null_case.append(inventory_cases_dict.get(case[1]))
            self.__cases_stock = null_case
        inventory_dict["CASES"] = inventory_cases_dict

        # need to add key/value pairs to inventory for cpu
        inventory_cpu_dict = {}
        null_cpu = []
        for cpu in self.__cpu:
            inventory_cpu_dict[cpu[1]] = 10
            null_cpu.append((inventory_cpu_dict.get(cpu[1])))
            self.__cpu_stock = null_cpu
        inventory_dict["CPU"] = inventory_cpu_dict



        # need to add key/value pairs to inventory for motherboards
        inventory_motherboards_dict = {}
        null_motherboard = []
        for motherboard in self.__motherboards:
            inventory_motherboards_dict[motherboard[1]] = 10
            null_motherboard.append((inventory_motherboards_dict.get(motherboard[1])))
            self.__motherboards_stock = null_motherboard
        inventory_dict["MOTHERBOARDS"] = inventory_motherboards_dict

        # need to add key/value pairs to inventory for cooling
        inventory_cooling_dict = {}
        null_cooling = []
        for cooling in self.__cooling:
            inventory_cooling_dict[cooling[1]] = 10
            null_cooling.append((inventory_cooling_dict.get(cooling[1])))
            self.__cooling_stock = null_cooling
        inventory_dict["COOLING"] = inventory_cooling_dict

        # need to add key/value pairs to inventory for memory
        inventory_memory_dict = {}
        null_memory = []
        for memory in self.__memory:
            inventory_memory_dict[memory[1]] = 10
            null_memory.append((inventory_memory_dict.get(memory[1])))
            self.__memory_stock = null_memory
        inventory_dict["MEMORY"] = inventory_memory_dict

        # need to add key/value pairs to inventory for gpu
        inventory_gpu_dict = {}
        null_gpu = []
        for gpu in self.__gpu:
            inventory_gpu_dict[gpu[1]] = 10
            null_gpu.append((inventory_gpu_dict.get(gpu[1])))
            self.__gpu_stock = null_gpu
        inventory_dict["GPU"] = inventory_gpu_dict

        # need to add key/value pairs to inventory for primary storage
        inventory_storage_dict = {}
        null_storage = []
        for storage in self.__primary_storage:
            inventory_storage_dict[storage[1]] = 10
            null_storage.append((inventory_storage_dict.get(storage[1])))
            self.__storage_stock = null_storage
        inventory_dict["STORAGE"] = inventory_storage_dict

        # need to add key/value pairs to inventory for power supply
        inventory_power_dict = {}
        null_power = []
        for power in self.__power_supply:
            inventory_power_dict[power[1]] = 10
            null_power.append((inventory_power_dict.get(power[1])))
            self.__power_stock = null_power
        inventory_dict["POWER"] = inventory_power_dict

        # need to add key/value pairs to inventory for op sys
        inventory_opsys_dict = {}
        null_opsys = []
        for opsys in self.__opsys:
            inventory_opsys_dict[opsys[1]] = 10
            null_opsys.append((inventory_opsys_dict.get(opsys[1])))
            self.__opsys_stock = null_opsys
        inventory_dict["OPSYS"] = inventory_opsys_dict

        # need to add key/value pairs to inventory for keyboards
        inventory_keyboards_dict = {}
        null_keyboards = []
        for keyboard in self.__keyboards:
            inventory_keyboards_dict[keyboard[1]] = 10
            null_keyboards.append((inventory_keyboards_dict.get(keyboard[1])))
            self.__keyboard_stock = null_keyboards
        inventory_dict["KEYBOARDS"] = inventory_keyboards_dict

        # need to add key/value pairs to inventory for mouse accessories
        inventory_mouse_dict = {}
        null_mouse = []
        for mouse_accessory in self.__mouse:
            inventory_mouse_dict[mouse_accessory[1]] = 10
            null_mouse.append((inventory_mouse_dict.get(mouse_accessory[1])))
            self.__mouse_stock_stock = null_mouse
        inventory_dict["MOUSE"] = inventory_mouse_dict

        #need to add to cases_stock

        db["INVENTORY"] = inventory_dict

        db.close()

    def update_inventory(self):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        self.__cases_stock = list(inventory_dict["CASES"].values())
        self.__cpu_stock = list(inventory_dict["CPU"].values())
        self.__motherboards_stock = list(inventory_dict["MOTHERBOARDS"].values())
        self.__cooling_stock = list(inventory_dict["COOLING"].values())
        self.__memory_stock= list(inventory_dict["MEMORY"].values())
        self.__gpu_stock = list(inventory_dict["GPU"].values())
        self.__storage_stock = list(inventory_dict["STORAGE"].values())
        self.__power_stock = list(inventory_dict["POWER"].values())
        self.__opsys_stock = list(inventory_dict["OPSYS"].values())
        self.__keyboard_stock = list(inventory_dict["KEYBOARDS"].values())
        self.__mouse_stock = list(inventory_dict["MOUSE"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    # case inventory
    def get_cases(self):
        return self.__cases

    def set_available_cases(self):
        cases = []
        for case in self.__cases:
            case_index = self.__cases.index(case)
            if self.__cases_stock[case_index] != 0:
                cases.append(case)
            else:
                pass
        self.__available_cases = cases

    def get_available_cases(self):
        return self.__available_cases

    def get_case_stock(self):
        return self.__cases_stock

    def get_indi_case_stock(self, case):
        return self.__cases_stock[self.__cases.index(case)]

    def decrement_case_stock(self, case):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["CASES"][case] -= 1
        self.__cases_stock = list(inventory_dict["CASES"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_case_stock(self, case):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["CASES"][case] += 1
        self.__cases_stock = list(inventory_dict["CASES"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()
#####################################################################################################################################################################################
# cpu inventory
    def get_cpu(self):
        return self.__cpu

    def set_available_cpu(self):
        cpu_array = []
        for cpu in self.__cpu:
            cpu_index = self.__cpu.index(cpu)
            if self.__cpu_stock[cpu_index] != 0:
                cpu_array.append(cpu)
            else:
                pass
        self.__available_cpu = cpu_array

    def get_available_cpu(self):
        return self.__available_cpu

    def get_cpu_stock(self):
        return self.__cpu_stock

    def get_indi_cpu_stock(self, cpu):
        return self.__cpu_stock[self.__cpu.index(cpu)]

    def decrement_cpu_stock(self, cpu):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["CPU"][cpu] -= 1
        self.__cpu_stock = list(inventory_dict["CPU"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_cpu_stock(self, cpu):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["CPU"][cpu] += 1
        self.__cpu_stock = list(inventory_dict["CPU"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    #####################################################################################################################################################################################
    #  motherboard inventory
    def get_motherboards(self):
        return self.__motherboards

    def set_available_motherboards(self):
        motherboards = []
        for motherboard in self.__motherboards:
            motherboard_index = self.__motherboards.index(motherboard)
            if self.__motherboards_stock[motherboard_index] != 0:
                motherboards.append(motherboard)
            else:
                pass
        self.__available_motherboards = motherboards

    def get_available_motherboards(self):
        return self.__available_motherboards

    def get_motherboard_stock(self):
        return self.__motherboards_stock

    def get_indi_motherboard_stock(self, motherboard):
        return self.__motherboards_stock[self.__motherboards.index(motherboard)]

    def decrement_motherboard_stock(self,motherboard):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["MOTHERBOARDS"][motherboard] -= 1
        self.__motherboards_stock = list(inventory_dict["MOTHERBOARDS"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_motherboard_stock(self,motherboard):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["MOTHERBOARDS"][motherboard] += 1
        self.__motherboards_stock = list(inventory_dict["MOTHERBOARDS"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

#####################################################################################################################################################################################
# cooling inventory
    def get_cooling(self):
        return self.__cooling

    def set_available_cooling(self):
        coolings = []
        for cooling in self.__cooling:
            cooling_index = self.__cooling.index(cooling)
            if self.__cooling_stock[cooling_index] != 0:
                coolings.append(cooling)
            else:
                pass
        self.__available_cooling = coolings

    def get_available_cooling(self):
        return self.__available_cooling

    def get_cooling_stock(self):
        return self.__cooling_stock

    def get_indi_cooling_stock(self, cooling):
        return self.__cooling_stock[self.__cooling.index(cooling)]

    def decrement_cooling_stock(self, cooling):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["COOLING"][cooling] -= 1
        self.__cooling_stock = list(inventory_dict["COOLING"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_cooling_stock(self, cooling):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["COOLING"][cooling] += 1
        self.__cooling_stock = list(inventory_dict["COOLING"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

#####################################################################################################################################################################################
# memory inventory
    def get_memory(self):
        return self.__memory

    def set_available_memory(self):
        memorys = []
        for memory in self.__memory:
            memory_index = self.__memory.index(memory)
            if self.__memory_stock[memory_index] != 0:
                memorys.append(memory)
            else:
                pass
        self.__available_memory = memorys

    def get_available_memory(self):
        return self.__available_memory

    def get_memory_stock(self):
        return self.__memory_stock

    def get_indi_memory_stock(self, memory):
        return self.__memory_stock[self.__memory.index(memory)]

    def decrement_memory_stock(self, memory):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["MEMORY"][memory] -= 1
        self.__memory_stock = list(inventory_dict["MEMORY"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_memory_stock(self, memory):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["MEMORY"][memory] += 1
        self.__memory_stock = list(inventory_dict["MEMORY"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

#####################################################################################################################################################################################
# gpu inventory
    def get_gpu(self):
        return self.__gpu

    def set_available_gpu(self):
        gpus = []
        for gpu in self.__gpu:
            gpu_index = self.__gpu.index(gpu)
            if self.__gpu_stock[gpu_index] != 0:
                gpus.append(gpu)
            else:
                pass
        self.__available_gpu = gpus

    def get_available_gpu(self):
        return self.__available_gpu

    def get_gpu_stock(self):
        return self.__gpu_stock

    def get_indi_gpu_stock(self, gpu):
        return self.__gpu_stock[self.__gpu.index(gpu)]

    def decrement_gpu_stock(self, gpu):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["GPU"][gpu] -= 1
        self.__gpu_stock = list(inventory_dict["GPU"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_gpu_stock(self, gpu):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["GPU"][gpu] += 1
        self.__gpu_stock = list(inventory_dict["GPU"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()


#####################################################################################################################################################################################
# storage inventory
    def get_storage(self):
        return self.__primary_storage

    def set_available_storage(self):
        storages = []
        for storage in self.__primary_storage:
            storage_index = self.__primary_storage.index(storage)
            if self.__storage_stock[storage_index] != 0:
                storages.append(storage)
            else:
                pass
        self.__available_storage = storages

    def get_available_storage(self):
        return self.__available_storage

    def get_storage_stock(self):
        return self.__storage_stock

    def get_indi_storage_stock(self, storage):
        return self.__storage_stock[self.__primary_storage.index(storage)]

    def decrement_storage_stock(self, storage):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["STORAGE"][storage] -= 1
        self.__storage_stock = list(inventory_dict["STORAGE"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_storage_stock(self, storage):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["STORAGE"][storage] += 1
        self.__storage_stock = list(inventory_dict["STORAGE"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()


#####################################################################################################################################################################################
# power inventory
    def get_power(self):
        return self.__power_supply

    def set_available_power(self):
        powers = []
        for power in self.__power_supply:
            power_index = self.__power_supply.index(power)
            if self.__power_stock[power_index] != 0:
                powers.append(power)
            else:
                pass
        self.__available_power = powers

    def get_available_power(self):
        return self.__available_power

    def get_power_stock(self):
        return self.__power_stock

    def get_indi_power_stock(self, power):
        return self.__power_stock[self.__power_supply.index(power)]

    def decrement_power_stock(self, power):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["POWER"][power] -= 1
        self.__power_stock = list(inventory_dict["POWER"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_power_stock(self, power):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["POWER"][power] += 1
        self.__power_stock = list(inventory_dict["POWER"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()


#####################################################################################################################################################################################
# opsys inventory
    def get_opsys(self):
        return self.__opsys

    def set_available_opsys(self):
        opsyss = []
        for opsys in self.__opsys:
            opsys_index = self.__opsys.index(opsys)
            if self.__opsys_stock[opsys_index] != 0:
                opsyss.append(opsys)
            else:
                pass
        self.__available_opsys = opsyss

    def get_available_opsys(self):
        return self.__available_opsys

    def get_opsys_stock(self):
        return self.__opsys_stock

    def get_indi_opsys_stock(self, opsys):
        return self.__opsys_stock[self.__opsys.index(opsys)]

    def decrement_opsys_stock(self, opsys):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["OPSYS"][opsys] -= 1
        self.__opsys_stock = list(inventory_dict["OPSYS"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_opsys_stock(self, opsys):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["OPSYS"][opsys] += 1
        self.__opsys_stock = list(inventory_dict["OPSYS"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

#####################################################################################################################################################################################
# keyboard inventory
    def get_keyboards(self):
        return self.__keyboards

    def set_available_keyboards(self):
        keyboards_list = []
        for keyboard in self.__keyboards:
            keyboard_index = self.__keyboards.index(keyboard)
            if self.__keyboard_stock[keyboard_index] != 0:
                keyboards_list.append(keyboard)
            else:
                pass
        self.__available_keyboards = keyboards_list

    def get_available_keyboards(self):
        return self.__available_keyboards

    def get_keyboard_stock(self):
        return self.__keyboard_stock

    def get_indi_keyboard_stock(self, keyboard):
        return self.__keyboard_stock[self.__keyboards.index(keyboard)]

    def decrement_keyboard_stock(self, keyboard):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["KEYBOARDS"][keyboard] -= 1
        self.__keyboard_stock = list(inventory_dict["KEYBOARDS"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_keyboard_stock(self, keyboard):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["KEYBOARDS"][keyboard] += 1
        self.__keyboard_stock = list(inventory_dict["KEYBOARDS"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()


#####################################################################################################################################################################################
# mouse inventory
    def get_mouse(self):
        return self.__mouse

    def set_available_mice(self):
        mice_list = []
        for mouse_accesory in self.__mouse:
            mouse_index = self.__mouse.index(mouse_accesory)
            if self.__mouse_stock[mouse_index] != 0:
                mice_list.append(mouse_accesory)
            else:
                pass
        self.__available_mouse = mice_list

    def get_available_mice(self):
        return self.__available_mouse

    def get_mice_stock(self):
        return self.__mouse_stock

    def get_indi_mouse_stock(self, mouse):
        return self.__mouse_stock[self.__mouse.index(mouse)]

    def decrement_mouse_stock(self, mouse):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["MOUSE"][mouse] -= 1
        self.__mouse_stock = list(inventory_dict["MOUSE"].values())


        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()

    def increment_mouse_stock(self, mouse):
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        inventory_dict["MOUSE"][mouse] += 1
        self.__mouse_stock = list(inventory_dict["MOUSE"].values())

        print(inventory_dict)

        db["INVENTORY"] = inventory_dict
        db.close()
