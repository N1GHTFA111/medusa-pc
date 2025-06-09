class PCShop:
    def __init__(self):
        self.num_of_floors = 2
        self.location = "Central Business District"
        self.price_range = "S$1500-S$8000"
        self.sponsors = "Corsair"
        self.edit_key = "Enabled"

    # getter and setters: floors
    def get_num_of_floors(self):
        if self.edit_key == "Enabled":
            return "Number of floors: " + str(self.num_of_floors)
        else:
            print("Private method unauthorized access")

    def set_num_of_floors(self, floors):
        if self.edit_key == "Enabled":
            self.num_of_floors = floors
        else:
            print("Private method unauthorized access")

    # getter and setters: location
    def get_location(self):
        if self.edit_key == "Enabled":
            return "Location: " + str(self.location)
        else:
            print("Private method unauthorized access")

    def set_location(self, new_loc):
        if self.edit_key == "Enabled":
            self.location = new_loc
        else:
            print("Private method unauthorized access")

    # getter and setters: price range
    def get_price_range(self):
        if self.edit_key == "Enabled":
            return "Price Range: " + str(self.price_range)
        else:
            print("Private method unauthorized access")

    # getter and setters: sponsors
    def get_sponsors(self):
        if self.edit_key == "Enabled":
            return "Sponsors: " + str(self.sponsors)
        else:
            print("Private method unauthorized access")

    def set_sponsors(self, new_sponsors):
        if self.edit_key == "Enabled":
            self.sponsors = new_sponsors
        else:
            print("Private method unauthorized access")
