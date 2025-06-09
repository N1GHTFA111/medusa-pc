class Account:
    def __init__(self, account_email, account_id, account_status):
        self.__account_email = account_email
        self.__account_id = account_id
        self.__account_status = account_status

    def get_account_id(self):
        return self.__account_id

    def get_account_status(self):
        return self.__account_status

    def set_account_id(self, value):
        self.__account_id = value

    def set_account_status(self, value):
        self.__account_status = value
