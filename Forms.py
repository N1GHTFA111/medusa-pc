from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, FloatField, \
    DecimalRangeField
from wtforms.fields import EmailField, DateField, PasswordField, SubmitField
from PC_classes import Case, CPU, GPU, Motherboard, Power_Supply, storage, cooling, Memory, Opsys, Wifi_card
from Inventory import Inventory


class CreateLoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired()])

class EmailVerificationForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])

class ForgetPasswordForm(Form):
    password = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired()])
    confirm_password = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired()])


class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(), validators.EqualTo('password_confirm', message='Passwords do not match. Retype Password.')])
    password_confirm = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(), ])
    address = StringField('Address', [validators.Length(min=1, max=200), validators.DataRequired()])
    country = StringField('Country', [validators.Length(min=1, max=200), validators.DataRequired()])
    state = StringField('State', [validators.Length(min=1, max=200), validators.DataRequired()])
    zip_code = StringField('Zip Code', [validators.Length(min=1, max=200), validators.DataRequired()])
    company = StringField('Company (Put None if N.A)', [validators.Length(min=1, max=200), validators.DataRequired()])
    phone = StringField('Phone Number (in this format: +65 12345678)', [validators.Length(min=1, max=200), validators.DataRequired()])

class CreateAdminForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(),
                                          validators.EqualTo('password_confirm',
                                                             message='Passwords do not match. Retype Password.')])
    password_confirm = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(), ])
    address = StringField('Address', [validators.Length(min=1, max=200), validators.DataRequired()])
    country = StringField('Country', [validators.Length(min=1, max=200), validators.DataRequired()])
    state = StringField('State', [validators.Length(min=1, max=200), validators.DataRequired()])
    zip_code = StringField('Zip Code', [validators.Length(min=1, max=200), validators.DataRequired()])
    phone = StringField('Phone Number (in this format: +65 12345678)',
                        [validators.Length(min=1, max=200), validators.DataRequired()])

class UpdateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(), validators.EqualTo('password_confirm', message='Passwords do not match. Retype Password.')])
    password_confirm = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(), ])
    address = StringField('Address', [validators.Length(min=1, max=200), validators.DataRequired()])
    country = StringField('Country', [validators.Length(min=1, max=200), validators.DataRequired()])
    state = StringField('State', [validators.Length(min=1, max=200), validators.DataRequired()])
    zip_code = StringField('Zip Code', [validators.Length(min=1, max=200), validators.DataRequired()])
    company = StringField('Company (Put None if N.A)', [validators.Length(min=1, max=200), validators.DataRequired()])
    phone = StringField('Phone Number (in this format: +65 12345678)',[validators.Length(min=1, max=200), validators.DataRequired()])

class UpdateAdminForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(), validators.EqualTo('password_confirm', message='Passwords do not match. Retype Password.')])
    password_confirm = PasswordField('Password', [validators.Length(min=1, max=200), validators.DataRequired(), ])
    address = StringField('Address', [validators.Length(min=1, max=200), validators.DataRequired()])
    country = StringField('Country', [validators.Length(min=1, max=200), validators.DataRequired()])
    state = StringField('State', [validators.Length(min=1, max=200), validators.DataRequired()])
    zip_code = StringField('Zip Code', [validators.Length(min=1, max=200), validators.DataRequired()])
    company = StringField('Company (Put None if N.A)', [validators.Length(min=1, max=200), validators.DataRequired()])
    phone = StringField('Phone Number (in this format: +65 12345678)',[validators.Length(min=1, max=200), validators.DataRequired()])

class ConfigurePCForm(Form):
    description = RadioField('Description', choices=[("Intel Tier 1", "Intel Tier 1"), ( "Intel Tier 2", 'Intel Tier 2'),], default='Intel Tier 1')

    #getting available cases
    # case_choices = inventory.get_available_cases()
    case = RadioField('Case', validators=[validators.InputRequired()])

    cpu = RadioField('CPU', choices=[("599,Intel i7-12700", "Intel i7-12700"), ('B', 'Beta'),], default="599,Intel i7-12700")

    #getting available motherboards
    motherboard = RadioField('Motherboard', validators=[validators.InputRequired()])

    cooling = RadioField('Cooling', choices=[("39,ID-Cooling SE-224-XT Black V2 Fan x1", "ID-Cooling SE-224-XT Black V2 Fan x1"), ('B', 'Beta'),], default="39,ID-Cooling SE-224-XT Black V2 Fan x1")
    memory = RadioField('Memory', choices=[("109,Corsair Vengeance LPX 3200 CL16 Intel/AMD 16GB", "Corsair Vengeance LPX 3200 CL16 Intel/AMD 16GB"), ('B', 'Beta'),], default="109,Corsair Vengeance LPX 3200 CL16 Intel/AMD 16GB")
    gpu = RadioField('Graphics Card', choices=[("269,Asus TUF Gaming GTX1650 OC 4GB", "Asus TUF Gaming GTX1650 OC 4GB"), ('B', 'Beta'),], default="269,Asus TUF Gaming GTX1650 OC 4GB")
    primary_storage = RadioField('Primary Storage', choices=[("199,Samsung 980 Pro 1TB", "Samsung 980 Pro 1TB"), ('B', 'Beta'),], default="199,Samsung 980 Pro 1TB")
    power_supply = RadioField('Power Supply', choices=[("129,Asus TUF Gaming 750W 80+Bronze", 'Asus TUF Gaming 750W 80+Bronze'), ('B', 'Beta'),], default="129,Asus TUF Gaming 750W 80+Bronze")
    op_sys = RadioField('Operating System', choices=[("100,Windows 11", "Windows 11"), ('B', 'Beta'),], default="100,Windows 11")
    wifi_bluetooth = RadioField('Wifi and Bluetooth', choices=[("0,No Wifi Card Needed","No Wifi Card Needed"),], default="0,No Wifi Card Needed")

    # #very important
    # @classmethod
    # def new(cls):
    #     #create instance of form
    #     form = cls()
    #     form.case.choices = get_available_cases()
    #
    #     #update all choices
    #     return form

class CreateShippingDate(Form):
    collection_type = RadioField('Collection Type', choices=[("Delivery", "Delivery"), ('Pick-Up', 'Pick-Up'), ], default="Delivery")
    shipping_date = DateField("Shipping/Collection Date", format="%Y-%m-%d")
    shipping_time = RadioField('Shipping/Collection Time', choices=[("9am to 12pm", "9am to 12pm"), ('2pm to 5pm', '2pm to 5pm')], default="9am to 12pm")
    destination_address = StringField('Destination Address', [validators.Length(min=1, max=200), validators.DataRequired()])
    voucher_form = StringField('Voucher ID', [validators.Length(min=1, max=200), validators.DataRequired()])

class CreateCouponOrPromoPercent(Form):
    name_of_discount = StringField('Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    discount_amount = FloatField('Amount', [validators.DataRequired(), validators.NumberRange(min=1, max=100)])
    type_of_discount = RadioField('Type of Discount', choices=[("Promo Code", "Promo Code"), ('Coupon', 'Coupon'), ], default="Promo Code")
    discount_code = StringField('Code', [validators.Length(min=1, max=200), validators.DataRequired()])
    points_required = IntegerField('Points Required', [validators.DataRequired(), validators.NumberRange(min=1, max=1000)])


class CreateFeedbackForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200), validators.DataRequired()])
    description = StringField('Description', [validators.Length(min=1, max=200), validators.DataRequired()])
    rating = IntegerField("Rating (1-10)", [validators.DataRequired(), validators.NumberRange(min=1, max=10)])

class UpdateFeedbackForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200), validators.DataRequired()])
    description = StringField('Title', [validators.Length(min=1, max=200), validators.DataRequired()])
    rating = IntegerField("Rating (1-10)", [validators.DataRequired(), validators.NumberRange(min=1, max=10)])

class CreateProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=200), validators.DataRequired()])
    price = IntegerField("Price", [validators.DataRequired()])
    category = RadioField('Category', choices=[("CASES", "CASES"), ('CPU', 'CPU'),("MOTHERBOARDS", "MOTHERBOARDS"), ('COOLING', 'COOLING'),("MEMORY", "MEMORY"), ('GPU', 'GPU'),("STORAGE", "STORAGE"), ('POWER', 'POWER'),("OPSYS", "OPSYS"), ('KEYBOARDS', 'KEYBOARDS'), ('MOUSE', 'MOUSE'),], default="CASES")

# class ConfigurePCForm(Form):
#     description = RadioField('Description', choices=[("Intel Tier 1", "Intel Tier 1"), ( "Intel Tier 2", 'Intel Tier 2'),], default='Intel Tier 1')
#
#     case1 = Case.Case(case_price=140, case_model='Corsair 4000D Airflow')
#     case1_options = ['Corsair 4000D Airflow', 140]
#     case = RadioField('Case', choices=[(case1_options, 'Corsair 4000D Airflow'), ('B', 'Beta'),], default=case1_options)
#
#     cpu1 = CPU.CPU(cpu_name='Intel i7-12700', cpu_price=599)
#     cpu = RadioField('CPU', choices=[(cpu1, "Intel i7-12700"), ('B', 'Beta'),], default=cpu1)
#
#     motherboard1 = Motherboard.Motherboard(model='Asus Prime Z790M-Plus D4-CSM', price=379)
#     motherboard = RadioField('Motherboard', choices=[(motherboard1, "Asus Prime Z790M-Plus D4-CSM"), ('B', 'Beta'),], default=motherboard1)
#
#     cooling1 = cooling.Cooling(cooling_name='ID-Cooling SE-224-XT Black V2 Fan x1', cooling_price=39)
#     cooling = RadioField('Cooling', choices=[(cooling1, "ID-Cooling SE-224-XT Black V2 Fan x1"), ('B', 'Beta'),], default=cooling1)
#
#     memory1 = Memory.Memory(name="Corsair Vengeance LPX 3200 CL16 Intel/AMD", price=109)
#     memory = RadioField('Memory', choices=[(memory1, "Corsair Vengeance LPX 3200 CL16 Intel/AMD"), ('B', 'Beta'),], default=memory1)
#
#     gpu1 = GPU.GPU(gpu_name="Asus TUF Gaming GTX1650 OC 4GB", gpu_price=269)
#     gpu = RadioField('Graphics Card', choices=[(gpu1, "Asus TUF Gaming GTX1650 OC 4GB"), ('B', 'Beta'),], default=gpu1)
#
#     storage1 = storage.Storage(storage_name="Samsung 980 Pro 1TB", storage_price=199)
#     primary_storage = RadioField('Primary Storage', choices=[(storage1, "Samsung 980 Pro 1TB"), ('B', 'Beta'),], default=storage1)
#
#     power_supply1 = Power_Supply.power_supply(name='Asus TUF Gaming 750W 80+Bronze', price=129)
#     power_supply = RadioField('Power Supply', choices=[(power_supply1, 'Asus TUF Gaming 750W 80+Bronze'), ('B', 'Beta'),], default=power_supply1)
#
#     op_sys1 = Opsys.OpSys(name="Windows 11", price=100)
#     op_sys = RadioField('Operating System', choices=[(op_sys1, "Windows 11"), ('B', 'Beta'),], default=op_sys1)
#
#     wifi_bluetooth1 = Wifi_card.wifi_card(name="None", price=0)
#     wifi_bluetooth = RadioField('Wifi and Bluetooth', choices=[(wifi_bluetooth1, "None"), ('B', 'Beta'),], default=wifi_bluetooth1)
