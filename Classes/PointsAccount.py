from Classes.Account import Account

class PointsAccount(Account):
    def __init__(self, account_email, account_id, account_status):
        super().__init__(account_email, account_id, account_status)
        self.__points = 0

    def get_points(self):
        return self.__points

    def set_points(self, value):
        self.__points = value
