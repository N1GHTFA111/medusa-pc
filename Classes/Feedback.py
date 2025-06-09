class Feedback:
    Id = 0

    def __init__(self, title, description, author, date_of_creation, rating, code):
        Feedback.Id += 1
        self.__id = Feedback.Id
        self.__title = title
        self.__description = description
        self.__author = author
        self.__date_of_creation = date_of_creation
        self.__rating = rating
        self.__feedback_code = code

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_author(self):
        return self.__author

    def get_date_of_creation(self):
        return self.__date_of_creation

    def get_rating(self):
        return self.__rating

    def get_code(self):
        return self.__feedback_code

    def set_id(self, new_id):
        self.__id = new_id

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def set_author(self, author):
        self.__author = author

    def set_date_of_creation(self, date):
        self.__date_of_creation = date

    def set_rating(self, rating):
        self.__rating = rating

    def set_code(self, code):
        self.__feedback_code = code

