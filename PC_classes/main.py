# PC shop
# PC contains:
# 1. Case (done)
# 2. Motherboard
# 3. CPU (done)
# 4. GPU (done)
# 5. storage (done)
# 6. Cooling (fan vs water) (done)
# 7. Wifi card
# 8. power supply (half-done)
# 9. monitor
# 10. keyboard and mouse set
# all power unit in w (watt)

# import classes
import PC_Shop
import Computer

# init shop
pc_Shop = PC_Shop.PCShop()
print(pc_Shop.get_num_of_floors())

new_pc = Computer.Computer()
new_pc.set_case_model("Delta")


print(new_pc.get_case_model())

print(new_pc.get_gpu_model())

print(new_pc.get_cpu_power_range())

print(new_pc.get_cooling_type())

# print(new_pc.get_cpu_model())
#
# print(new_pc.get_GPU_model())
#
# print(new_pc.get_case_model())
#
# print(new_pc.get_storage_name())
#
# print(new_pc.get_cooling_type())

# if pc_Shop == PC_Shop.PCShop:
#     choice = input("Do you want a Prebuilt (1) or DIY PC (2): ")
#     if choice == "1":
#         print("Building Computer")
#     else:
#         print("Invalid Choice")
#
# else:
#     print("Store is not opened")
