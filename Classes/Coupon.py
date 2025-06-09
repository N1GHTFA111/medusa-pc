class Coupon:
    def __init__(self, coupon_id, name, percent):
        self.__id = coupon_id
        self.__name = name
        self.__percent = percent
        self.__expiry_date = "N.A."
        self.__date_of_creation = None
        self.__status = None
        self.__points_required = None

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_percent(self):
        return self.__percent

    def get_expiry_date(self):
        return self.__expiry_date

    def get_date_of_creation(self):
        return self.__date_of_creation

    def get_status(self):
        return self.__status

    def get_required_points(self):
        return self.__points_required

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_percent(self, percent):
        self.__percent = percent

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def set_date_of_creation(self, date):
        self.__date_of_creation = date

    def set_status_to_active(self):
        self.__status = "Active"

    def set_status_to_expired(self):
        self.__status = "Expired"

    def set_required_points(self, points):
        self.__points_required = points
