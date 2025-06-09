from Classes.Coupon import Coupon

class Promo(Coupon):
    def __init__(self, coupon_id,  name, percent, code):
        super().__init__(coupon_id, name, percent)
        self.__voucher_code = code

    def get_voucher_code(self):
        return self.__voucher_code

    def set_voucher_code(self, code):
        self.__voucher_code = code
