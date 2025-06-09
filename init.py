import base64
import multiprocessing
import os.path
import string
from uuid import uuid4

import flask_login
import jinja2
from flask import Flask, render_template, request, url_for, redirect, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin as UM
import shelve
from flask_sqlalchemy import SQLAlchemy
from Crypto.Hash import SHA256
from base64 import b64encode
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from sqlalchemy import ForeignKey

from Classes.Feedback import Feedback
from Classes.Promo import Promo
from Classes.Coupon import  Coupon
from Classes.Shipment import Shipment
from Classes.PointsAccount import PointsAccount
from Forms import *
from PC_classes import *
from PC_classes.Computer import Computer
from PC_classes import Keyboard
from PC_classes import Mouse
from Item import Item
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import base64
import dateutil.parser
from Inventory import Inventory

#send email
from email.message import EmailMessage
import ssl
import smtplib

#modules to create pdf invoice
# basic functions
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page

# build pdf
from borb.pdf import PDF

# layout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal

# add image
from borb.pdf.canvas.layout.image.image import Image

# building the invoice
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import  Alignment
from datetime import datetime
import random

# adding color to pdf
from borb.pdf.canvas.color.color import HexColor, X11Color

# build item table
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell

# create outline
from borb.pdf.canvas.layout.annotation.link_annotation import DestinationType

# stripe checkout
import json
import stripe

import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'pricelist'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
inventory = Inventory()
# stripe checkout
stripe.api_key = os.environ.get('STRIPE_API_KEY')


def is_PC(item):
    return isinstance(item, Computer)

def check_for_invoice():
    if os.path.exists("invoice.pdf"):
        return True
    else:
        return False

def check_for_pricelist():
    if os.path.exists("pricelist/pricelist_test.txt"):
        return True
    else:
        return False

def convert_to_list(item):
    return list(item)

def isPromo(coupon):
    if isinstance(coupon, Promo):
        return True
    else:
        return False
def check_pts_account_balance(current_points, points_required):
    if current_points >= points_required:
        return True
    else:
        return False

def retrieve_voucher(voucher_key):
    return stripe.Coupon.retrieve(voucher_key)


# add these custom functions to jinja
app.jinja_env.globals.update(is_PC=is_PC)
app.jinja_env.globals.update(check_for_invoice=check_for_invoice)
app.jinja_env.globals.update(check_for_pricelist=check_for_pricelist)
app.jinja_env.globals.update(convert_to_list=convert_to_list)
app.jinja_env.globals.update(isPromo=isPromo)
app.jinja_env.globals.update(check_pts_account_balance=check_pts_account_balance)
app.jinja_env.globals.update(retrieve_voucher=retrieve_voucher)

# unlock the inventory system

# check if inventory exists
try:
    db_test = shelve.open('inventory.db', "r")
    db_test.close()
except:
    # if it does not exist, create the inventory
    inventory.create_inventory()

# update the inventory with the updated data
inventory.update_inventory()

# check if products.db exists
try:
    products_db = shelve.open('products.db', 'r')
    products_db.close()
    inventory.update_products()
except:
    inventory.gather_products()


#############################################
# AVAILABLE PARTS
#getting available parts
available_cases = inventory.set_available_cases()
available_cpu = inventory.set_available_cpu()
available_motherboards = inventory.set_available_motherboards()
available_cooling = inventory.set_available_cooling()
available_memory = inventory.set_available_memory()
available_gpu = inventory.set_available_gpu()
available_storage = inventory.set_available_storage()
available_power = inventory.set_available_power()
available_opsys = inventory.set_available_opsys()
available_keyboards = inventory.set_available_keyboards()
available_mice = inventory.set_available_mice()


# comparing passwords during login
def valid_password(input, database_pw):
    try:
        bcrypt_check(input, database_pw)
        print("Success")
        return True
    except ValueError:
        print("Not Success")
        return False

# Create UserModel database
# Contains the required getters and setters for the users

# base class that all user classes will inherit from
class UserModel(UM, db.Model):

    __tablename__ = "user_model"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(200), unique=True)
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    address = db.Column(db.String(200))
    country = db.Column(db.String(200))
    state = db.Column(db.String(200))
    zip_code = db.Column(db.String(200))
    company = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    role = db.Column(db.String(200))

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_address(self):
        return self.address

    def get_country(self):
        return self.country

    def get_state(self):
        return self.state

    def get_zip_code(self):
        return self.zip_code

    def get_company(self):
        return self.company

    def get_phone(self):
        return self.phone

    def get_role(self):
        return self.role

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def set_address(self, address):
        self.address = address

    def set_country(self, country):
        self.country = country

    def set_state(self, state):
        self.state = state

    def set_zip_code(self, zip_c):
        self.zip_code = zip_c

    def set_company(self, company):
        self.company = company

    def set_phone(self, phone):
        self.phone = phone

    def set_role(self, role):
        self.role = role

# These 2 classes will be used to double check the role of the logged in user

# a blueprint for the User and Guest Obj
class User(UserModel):
    __tablename__ = "USER"
    id = db.Column(db.Integer, ForeignKey('user_model.id'), primary_key=True)
    # account_id = db.Column(db.String(200), unique=True)

# a blueprint for the Admin Obj
class Admin(UserModel):
    __tablename__ = "ADMIN"
    id = db.Column(db.Integer, ForeignKey('user_model.id'), primary_key=True)


# create the UserModel database if it is not created yet
with app.app_context():
    db.create_all()

# migrate = Migrate(app, db, render_as_batch=True)

# for retrieval from the database
@login_manager.user_loader
def load_user(user_id):
    # db = shelve.open('user.db', 'c')
    # try:
    #     users_dict = db['Users']
    #     user = users_dict.get(user_id)
    #     db.close()
    #     return user
    # except:
    #     print("Error in retrieving the User from user.db")
    #
    # db.close()
    print(user_id)
    return UserModel.query.get(int(user_id))

# main index page
@app.route("/")
def index():
    return render_template("index.html")

# admin index page that only admin users can use, requires the secret code to access
@app.route("/admin")
def admin_index():
    return render_template("index_admin.html")

# register a user with the role of USER to use for the website
# only USER role users have a points account
@app.route('/registerUser', methods=["GET", "POST"])
def registerUser():

    # create a form for the user to register
    createuserform = CreateUserForm(request.form)
    if request.method == "POST" and createuserform.validate():
        # users_dict = {}
        # db = shelve.open('user.db', 'c')
        #
        # try:
        #     users_dict = db['Users']
        # except:
        #     print("Error in retrieving Users from user.db.")

        #hashing, salting and storing the password
        password = createuserform.password.data
        password = password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)
        # new_user = User.User(createuserform.first_name.data,
        #                  createuserform.last_name.data,
        #                  createuserform.email.data,
        #                  bcrypt_hash
        # )
        # users_dict[new_user.get_user_id()] = users_dict
        # db['Users'] = users_dict
        # db.close()

        new_user = User(first_name=createuserform.first_name.data,
                             last_name=createuserform.last_name.data,
                             email=createuserform.email.data,
                             password=bcrypt_hash,
                             address=createuserform.address.data,
                             country=createuserform.country.data,
                             state=createuserform.state.data,
                             zip_code = createuserform.zip_code.data,
                             company=createuserform.company.data,
                             phone=createuserform.phone.data,
                             role="USER")

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        # open or create the PointsAccounts.db
        pointsAccounts_dict = {}
        try:
            db_pointsAccounts = shelve.open("PointsAccounts.db", "w")
        except:
            db_pointsAccounts = shelve.open("PointsAccounts.db", "c")

        # try to retreive data from the db
        try:
            pointsAccounts_dict = db_pointsAccounts["Points_Accounts"]
        except:
            print("Could not retrieve points accounts from PointsAccounts.db")

        # create the pointsAccount for the user
        account_id = "ptsAcct_" + generate_random_string(10)
        new_pointsAccount = PointsAccount(account_email=new_user.get_email(), account_id=account_id, account_status="Active")
        pointsAccounts_dict[new_user.get_id()] = new_pointsAccount

        db_pointsAccounts["Points_Accounts"] = pointsAccounts_dict

        db_pointsAccounts.close()


        return redirect(url_for('get_dashboard', username=new_user.get_first_name()))
    return render_template("registerUser.html",form=createuserform, logged_in=current_user.is_authenticated)

@app.route('/registerAdmin', methods=["GET", "POST"])
def registerAdmin():
    createadminform = CreateAdminForm(request.form)
    if request.method == "POST" and createadminform.validate():
        password = createadminform.password.data
        password = password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)

        new_admin = Admin(first_name=createadminform.first_name.data,
                        last_name=createadminform.last_name.data,
                        email=createadminform.email.data,
                        password=bcrypt_hash,
                        address=createadminform.address.data,
                        country=createadminform.country.data,
                        state=createadminform.state.data,
                        zip_code=createadminform.zip_code.data,
                        company="Medusa Pte Ltd",
                        phone=createadminform.phone.data,
                        role="ADMIN")
        db.session.add(new_admin)
        db.session.commit()
        login_user(new_admin)
        return redirect(url_for('get_dashboard', username=new_admin.get_first_name()))
    return render_template("registerAdmin.html", form=createadminform, logged_in=current_user.is_authenticated)

def generate_random_string(size):
    ran_string = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    return ran_string

# For guest users, they must be able to auto login, they cannot update their user
@app.route('/registerGuest', methods=["GET", "POST"])
def registerGuest():

    if request.method == "GET":
        password = generate_random_string(10)
        password = password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)
        guest_name = "Guest-"+generate_random_string(12)

        new_guest = User(first_name=guest_name,
                        last_name="None",
                        email=guest_name+"@medusa.com",
                        password=bcrypt_hash,
                        address="None",
                        country="None",
                        state="None",
                        zip_code="None",
                        company="None",
                        phone="None",
                        role="GUEST")
        print(new_guest.get_id())
        db.session.add(new_guest)
        db.session.commit()
        login_user(new_guest)
        return redirect(url_for('get_dashboard', username=new_guest.get_first_name()))


# @app.route('/retrieveUser')
# def retrieveUsers():
#     users_dict = {}
#     db = shelve.open('user.db', 'r')
#     users_dict = db['Users']
#     db.close()
#
#     users_list = []
#     for key in users_dict:
#         user = users_dict.get(key)
#         users_list.append(user)
#     print(users_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    createloginform = CreateLoginForm(request.form)
    # if request.method == "POST" and createloginform.validate():
    #     users_dict = {}
    #     db = shelve.open('user.db', 'r')
    #
    #     try:
    #         users_dict = db['Users']
    #         email = createloginform.email.data
    #         password = createloginform.password.data
    #         password = password.encode('utf-8')
    #         b64pwd = b64encode(SHA256.new(password).digest())
    #         user = users_dict.
    #     except:
    #         print("Error in retrieving Users from user.db.")

    #if user already logged in
    if current_user.is_authenticated:
        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

    if request.method == "POST" and createloginform.validate():
        email = createloginform.email.data
        password = createloginform.password.data
        password = password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(password).digest())


        if email == "12345678@medusa.com":
            return redirect(url_for("admin_index"))

        user_in_db = UserModel.query.filter_by(email=email).first()
        if not user_in_db:
            flash("That email does not exist, please try again or register for an account")
            return redirect(url_for('login'))
        elif not valid_password(b64pwd, user_in_db.password):
            flash("Password Incorrect, please try again")
            return redirect(url_for('login'))
        else:
            login_user(user_in_db)
            print("Success")

             # open or create the PointsAccounts.db
            pointsAccounts_dict = {}
            try:
                db_pointsAccounts = shelve.open("PointsAccounts.db", "w")
            except:
                db_pointsAccounts = shelve.open("PointsAccounts.db", "c")

            # try to retreive data from the db
            try:
                pointsAccounts_dict = db_pointsAccounts["Points_Accounts"]
            except:
                print("Could not retrieve points accounts from PointsAccounts.db")

            # create the pointsAccount for the user
            try:
                tester = pointsAccounts_dict[current_user.get_id()]
            except KeyError:
                account_id = "ptsAcct_" + generate_random_string(10)
                new_pointsAccount = PointsAccount(account_email=current_user.get_email(), account_id=account_id, account_status="Active")
                pointsAccounts_dict[current_user.get_id()] = new_pointsAccount
                db_pointsAccounts["Points_Accounts"] = pointsAccounts_dict

                db_pointsAccounts.close()


            return redirect(url_for('get_dashboard', username=user_in_db.get_first_name()))
    return render_template("login.html",form=createloginform, logged_in=current_user.is_authenticated)


@app.route('/view_all_users/<path:username>')
@login_required
def user_management(username):
    current_user = username
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('index'))
    all_users = UserModel.query.all()
    count = 0
    admin_count = 0
    for user in all_users:
        count += 1
        if user.get_role() == "ADMIN":
            admin_count += 1
    return render_template('view_all_users.html', users_db=all_users, logged_in=flask_login.current_user.is_authenticated, username=flask_login.current_user.get_first_name(), user=str(current_user), count=count, admin_count=admin_count)


@app.route('/logout')
@login_required
def logout():
    if not(current_user.get_role() == "ADMIN" or current_user.get_role() == "USER" or current_user.get_role() == "GUEST"):
        return redirect(url_for('index'))
    logout_user()
    return redirect(url_for("index"))

@app.route('/updateUser', methods=["GET", "POST"])
@login_required
def updateUser():
    #exit if not a USER or ADMIN
    if not(current_user.get_role() == "ADMIN" or current_user.get_role() == "USER"):
        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

    updateuserform = UpdateUserForm(request.form)
    #if im updating
    if request.method == "POST" and updateuserform.validate():
        new_first_name = updateuserform.first_name.data
        new_last_name = updateuserform.last_name.data
        new_email = updateuserform.email.data
        new_password = updateuserform.password.data
        new_password = new_password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(new_password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)
        new_address = updateuserform.address.data
        new_country = updateuserform.country.data
        new_state = updateuserform.state.data
        new_zip_code = updateuserform.zip_code.data
        new_company = updateuserform.company.data
        new_phone = updateuserform.phone.data

        current_user_to_update = UserModel.query.filter_by(email=current_user.get_email()).first()
        # current_user_to_update.first_name = new_first_name
        # current_user_to_update.last_name = new_last_name
        # current_user_to_update.email = new_email
        # current_user_to_update.password = bcrypt_hash
        current_user_to_update.set_first_name(new_first_name)
        current_user_to_update.set_last_name(new_last_name)
        current_user_to_update.set_email(new_email)
        current_user_to_update.set_password(bcrypt_hash)
        current_user_to_update.set_address(new_address)
        current_user_to_update.set_country(new_country)
        current_user_to_update.set_state(new_state)
        current_user_to_update.set_zip_code(new_zip_code)
        current_user_to_update.set_company(new_company)
        current_user_to_update.set_phone(new_phone)

        db.session.commit()
        login_user(current_user_to_update)
        return redirect(url_for('get_dashboard', username=current_user_to_update.get_first_name(), logged_in=current_user.is_authenticated))
    else:
        current_user_to_update = UserModel.query.filter_by(email=current_user.email).first()
        updateuserform.first_name.data = current_user_to_update.get_first_name()
        updateuserform.last_name.data = current_user_to_update.get_last_name()
        updateuserform.email.data = current_user_to_update.get_email()
        updateuserform.address.data = current_user_to_update.get_address()
        updateuserform.country.data = current_user_to_update.get_country()
        updateuserform.state.data = current_user_to_update.get_state()
        updateuserform.zip_code.data = current_user_to_update.get_zip_code()
        updateuserform.company.data = current_user_to_update.get_company()
        updateuserform.phone.data = current_user_to_update.get_phone()
        # updateuserform.password = current_user_to_update.password

        return render_template("updateUser.html", username=current_user_to_update.get_first_name(), form=updateuserform, logged_in=current_user.is_authenticated)

@app.route('/updateUser_Admin/<email>', methods=['GET', 'POST'])
def updateUser_admin(email):
    #exit if not a USER or ADMIN
    if not(current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

    updateadminform = UpdateAdminForm(request.form)
    #if im updating
    if request.method == "POST" and updateadminform.validate():
        new_first_name = updateadminform.first_name.data
        new_last_name = updateadminform.last_name.data
        new_email = updateadminform.email.data
        new_password = updateadminform.password.data
        new_password = new_password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(new_password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)
        new_address = updateadminform.address.data
        new_country = updateadminform.country.data
        new_state = updateadminform.state.data
        new_zip_code = updateadminform.zip_code.data
        new_phone = updateadminform.phone.data

        current_user_to_update = UserModel.query.filter_by(email=email).first()
        # current_user_to_update.first_name = new_first_name
        # current_user_to_update.last_name = new_last_name
        # current_user_to_update.email = new_email
        # current_user_to_update.password = bcrypt_hash
        current_user_to_update.set_first_name(new_first_name)
        current_user_to_update.set_last_name(new_last_name)
        current_user_to_update.set_email(new_email)
        current_user_to_update.set_password(bcrypt_hash)
        current_user_to_update.set_address(new_address)
        current_user_to_update.set_country(new_country)
        current_user_to_update.set_state(new_state)
        current_user_to_update.set_zip_code(new_zip_code)
        current_user_to_update.set_phone(new_phone)

        db.session.commit()
        return redirect(url_for('get_dashboard', username=current_user_to_update.get_first_name(),  logged_in=current_user.is_authenticated))
    else:
        current_user_to_update = UserModel.query.filter_by(email=email).first()
        updateadminform.first_name.data = current_user_to_update.get_first_name()
        updateadminform.last_name.data = current_user_to_update.get_last_name()
        updateadminform.email.data = current_user_to_update.get_email()
        updateadminform.address.data = current_user_to_update.get_address()
        updateadminform.country.data = current_user_to_update.get_country()
        updateadminform.state.data = current_user_to_update.get_state()
        updateadminform.zip_code.data = current_user_to_update.get_zip_code()
        updateadminform.phone.data = current_user_to_update.get_phone()
        # updateuserform.password = current_user_to_update.password

        return render_template("updateAdmin.html", email=email, form=updateadminform,)

@app.route('/forgetpassword', methods=['GET', 'POST'])
def forget_password():
    email_verification_form = EmailVerificationForm(request.form)
    email = email_verification_form.email.data
    if request.method == "POST" and email_verification_form.validate():
        return redirect(url_for('send_reset_link', email=email))

    return render_template('email_verification.html', form=email_verification_form)

@app.route('/send_reset_link/<path:email>', methods=['GET', 'POST'])
def send_reset_link(email):
    email_sender = 'medusapc123@gmail.com'
    email_receiver = str(email)
    app_password = "hourgtepdumwweou"

    subject = "Below is the password recovery link for Medusa PC"
    body = f"""
    Click on this link to reset your password: http://127.0.0.1:5000/reset_password?email={email_receiver}
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, app_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        return render_template("email_success_sent.html")
    except:
        return render_template("email_failure_sent.html")


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')
    print(type(email))
    current_user_to_reset_password = UserModel.query.filter_by(email=email).first()

    forgetpasswordform = ForgetPasswordForm(request.form)
    if request.method == "POST" and forgetpasswordform.validate():
        while True:
            new_password = forgetpasswordform.password.data
            new_password_confirm = forgetpasswordform.confirm_password.data
            if new_password == new_password_confirm:
                break
            else:
                forgetpasswordform = ForgetPasswordForm(request.form)

        new_password = new_password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(new_password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)
        # print(str(bcrypt_hash))
        current_user_to_reset_password.set_password(bcrypt_hash)
        db.session.commit()
        login_user(current_user_to_reset_password)
        return redirect(url_for('get_dashboard', username=current_user_to_reset_password.get_first_name(), logged_in=current_user.is_authenticated))

    return render_template("forgot_password_form.html", form=forgetpasswordform)


@app.route('/deleteUser', methods=['GET', 'POST'])
@login_required
def deleteUser():
    if not(current_user.get_role() == "ADMIN" or current_user.get_role() == "USER" or current_user.get_role() == "GUEST"):
        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

    current_user_to_delete = UserModel.query.filter_by(email=current_user.get_email()).first()
    db.session.delete(current_user_to_delete)
    if current_user_to_delete.get_role() == "USER":
        db.session.delete(User.query.filter_by(id=current_user_to_delete.get_id()).first())
    elif current_user_to_delete.get_role() == "GUEST":
        print("Guest Deleted")
        db.session.delete(User.query.filter_by(id=current_user_to_delete.get_id()).first())
    elif current_user_to_delete.get_role() == "ADMIN":
        db.session.delete(Admin.query.filter_by(id=current_user_to_delete.get_id()).first())
    else:
        pass
    db.session.delete(current_user_to_delete)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/deleteUser_Admin/path:<email>', methods=['GET', 'POST'])
@login_required
def deleteUser_admin(email):
    if not(current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

    print(email)
    user_to_delete = UserModel.query.filter_by(email=email).first()

    print(user_to_delete.get_role())
    if user_to_delete.get_role() == "USER":
        db.session.delete(User.query.filter_by(id=user_to_delete.get_id()).first())
    elif user_to_delete.get_role() == "GUEST":
        print("Guest Deleted")
        # print(User.query.get(user_to_delete.get_id()))
        db.session.delete(User.query.filter_by(id=user_to_delete.get_id()).first())
    elif user_to_delete.get_role() == "ADMIN":
        db.session.delete(Admin.query.filter_by(id=user_to_delete.get_id()).first())
    else:
        pass
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

@app.route('/dashboard/<path:username>', methods=['GET', 'POST'])
@login_required
def get_dashboard(username):
    if not(flask_login.current_user.get_role() == "ADMIN" or flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        return redirect(url_for('login'))
    if flask_login.current_user.get_role() == "ADMIN":
        return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
    # print(flask_login.current_user.get_first_name())
    if username == flask_login.current_user.get_first_name():
        current_user = username
        print(current_user)
        return render_template("dashboard.html", user=str(current_user))
    else:
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

#dashboard section

#buying a custom pc
@app.route('/dashboard/<path:username>/CustomPC')
@login_required
def get_dashboard_custom_pc(username):
    if not(flask_login.current_user.get_role() == "ADMIN" or flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        return redirect(url_for('login'))
    if flask_login.current_user.get_role() == "ADMIN":
        return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
    current_user = username
    print(type(current_user))
    return render_template("dashboard_custom_pc.html", user=str(current_user))

#buying a part
@app.route('/dashboard/<path:username>/PCPart')
@login_required
def get_dashboard_pc_part(username):
    if not(flask_login.current_user.get_role() == "ADMIN" or flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        return redirect(url_for('login'))
    if flask_login.current_user.get_role() == "ADMIN":
        return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
    current_user = username
    print(type(current_user))
    return render_template("dashboard_pc_part.html", user=str(current_user), inventory=inventory)

#buying a accessory
@app.route('/dashboard/<path:username>/PCAccessory')
@login_required
def get_dashboard_pc_accessory(username):
    if not(flask_login.current_user.get_role() == "ADMIN" or flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        return redirect(url_for('login'))
    if flask_login.current_user.get_role() == "ADMIN":
        return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
    current_user = username
    print(type(current_user))
    return render_template("dashboard_accessories.html", user=str(current_user), inventory=inventory)

#creating a pc
@app.route('/dashboard/CreatePC', methods=["GET", "POST"])
@login_required
def create_custom_pc():
    if not(flask_login.current_user.get_role() == "ADMIN" or flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        return redirect(url_for('login'))
    if flask_login.current_user.get_role() == "ADMIN":
        return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
    # current_user_creating = UserModel.query.filter_by(email=current_user.get_email()).first()
    # current_user_id = current_user_creating.
    current_user_id = current_user.get_id()

    #update inventory available stock
    inventory.set_available_cases()
    inventory.set_available_cpu()
    inventory.set_available_motherboards()
    inventory.set_available_cooling()
    inventory.set_available_memory()
    inventory.set_available_gpu()
    inventory.set_available_storage()
    inventory.set_available_power()
    inventory.set_available_opsys()
    inventory.set_available_keyboards()
    inventory.set_available_mice()

    #initialize form with default options
    available_cases = inventory.get_available_cases()
    available_cpu = inventory.get_available_cpu()
    available_motherboards = inventory.get_available_motherboards()
    available_cooling = inventory.get_available_cooling()
    available_memory = inventory.get_available_memory()
    available_gpu = inventory.get_available_gpu()
    available_storage = inventory.get_available_storage()
    available_power = inventory.get_available_power()
    available_opsys = inventory.get_available_opsys()

    print(available_cases)

    print("Hey")
    print(available_motherboards)
    print(available_opsys)

    createpcform = ConfigurePCForm(request.form, case=available_cases[0][0], motherboard=available_motherboards[0][0],
                                   cooling=available_cooling[0][0], memory=available_memory[0][0],
                                   gpu=available_gpu[0][0],
                                   primary_storage=available_storage[0][0],
                                   power_supply=available_power[0][0],
                                   op_sys=available_opsys[0][0])
    # print(createpcform.case.choices)

    createpcform.case.choices = available_cases
    # print(createpcform.case.choices)
    createpcform.cpu.choices = available_cpu
    createpcform.motherboard.choices = available_motherboards
    createpcform.cooling.choices = available_cooling
    createpcform.memory.choices = available_memory
    createpcform.gpu.choices = available_gpu
    createpcform.primary_storage.choices = available_storage
    createpcform.power_supply.choices = available_power
    createpcform.op_sys.choices = available_opsys

    if request.method == "POST" and createpcform.validate():
        # for each user, a dictionary is added as the key value, dictionary will add their PC
        cart_dict = {}
        db = shelve.open('carts.db', 'c')

        try:
            cart_dict = db[current_user_id]
        except:
            print("Error in retrieving carts from carts.db.")

        #pc parts
        pc_description = createpcform.description.data

        pc_case = createpcform.case.data
        # pc_case_to_decrement = (pc_case, pc_case.split(",")[1])
        # print(pc_case_to_decrement)
        inventory.decrement_case_stock(pc_case.split(",")[1])
        # print(inventory.get_case_stock())

        pc_motherboard = createpcform.motherboard.data
        inventory.decrement_motherboard_stock(pc_motherboard.split(",")[1])

        pc_cpu = createpcform.cpu.data
        inventory.decrement_cpu_stock(pc_cpu.split(",")[1])

        pc_gpu = createpcform.gpu.data
        inventory.decrement_gpu_stock(pc_gpu.split(",")[1])

        pc_storage = createpcform.primary_storage.data
        inventory.decrement_storage_stock(pc_storage.split(",")[1])

        pc_cooling = createpcform.cooling.data
        inventory.decrement_cooling_stock(pc_cooling.split(",")[1])

        pc_power_supply = createpcform.power_supply.data
        inventory.decrement_power_stock(pc_power_supply.split(",")[1])

        pc_wifi = createpcform.wifi_bluetooth.data


        pc_op_sys = createpcform.op_sys.data
        inventory.decrement_opsys_stock(pc_op_sys.split(",")[1])

        pc_memory = createpcform.memory.data
        inventory.decrement_memory_stock(pc_memory.split(",")[1])

        new_pc = Computer(pc_case, pc_motherboard, pc_cpu, pc_gpu, pc_storage, pc_cooling, pc_power_supply, pc_wifi, pc_op_sys, pc_memory)
        new_pc.set_description(pc_description)

        # #calculate price
        # total_price = pc_case.get_price + pc_motherboard.get_price() + pc_cpu.get_price() + pc_gpu.get_price() + pc_storage.get_price() + pc_cooling.get_price() + pc_power_supply.get_price() + pc_wifi.get_price() + pc_op_sys.get_price() + pc_memory.get_price()
        total_price = int(pc_case.split(",")[0]) + int(pc_motherboard.split(",")[0]) + int(pc_cpu.split(",")[0]) + int(pc_storage.split(",")[0]) + int(pc_cooling.split(",")[0]) + int(pc_power_supply.split(",")[0]) + int(pc_wifi.split(",")[0]) + int(pc_op_sys.split(",")[0]) + int(pc_memory.split(",")[0])

        new_pc_item = Item(new_pc, pc_description, total_price)
        cart_dict[new_pc_item.get_id()] = new_pc_item
        #add back cart_dict to db
        # print(cart_dict)
        db[current_user_id] = cart_dict
        db.close()

        inventory.set_available_cases()
        inventory.set_available_cpu()
        inventory.set_available_motherboards()
        inventory.set_available_cooling()
        inventory.set_available_memory()
        inventory.set_available_gpu()
        inventory.set_available_storage()
        inventory.set_available_power()
        inventory.set_available_opsys()

        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))
    return render_template("createPC.html",form=createpcform, user=str(current_user))

#creating a pc
@app.route('/dashboard/CreatePart/<path:part_category>/<path:part_name>/<path:part_price>', methods=["GET", "POST"])
@login_required
def create_part(part_category, part_name, part_price):
    if not(flask_login.current_user.get_role() == "ADMIN" or flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        return redirect(url_for('login'))
    if flask_login.current_user.get_role() == "ADMIN":
        return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
    # current_user_creating = UserModel.query.filter_by(email=current_user.get_email()).first()
    # current_user_id = current_user_creating.
    current_user_id = current_user.get_id()

    # update inventory available stock
    inventory.set_available_cases()
    inventory.set_available_cpu()
    inventory.set_available_motherboards()
    inventory.set_available_cooling()
    inventory.set_available_memory()
    inventory.set_available_gpu()
    inventory.set_available_storage()
    inventory.set_available_power()
    inventory.set_available_opsys()
    inventory.set_available_keyboards()
    inventory.set_available_mice()

    #initialize form with default options
    available_cases = inventory.get_available_cases()
    available_cpu = inventory.get_available_cpu()
    available_motherboards = inventory.get_available_motherboards()
    available_cooling = inventory.get_available_cooling()
    available_memory = inventory.get_available_memory()
    available_gpu = inventory.get_available_gpu()
    available_storage = inventory.get_available_storage()
    available_power = inventory.get_available_power()
    available_opsys = inventory.get_available_opsys()


    if request.method == "POST":
        # for each user, a dictionary is added as the key value, dictionary will add their PC
        cart_dict = {}
        db = shelve.open('carts.db', 'c')

        try:
            cart_dict = db[current_user_id]
        except:
            print("Error in retrieving carts from carts.db.")

        # #calculate price
        # total_price = pc_case.get_price + pc_motherboard.get_price() + pc_cpu.get_price() + pc_gpu.get_price() + pc_storage.get_price() + pc_cooling.get_price() + pc_power_supply.get_price() + pc_wifi.get_price() + pc_op_sys.get_price() + pc_memory.get_price()
        print(part_name)
        print(part_price)

        total_price = int(part_price)
        print(total_price)

        new_part = ""

        if part_category == "CASES":
            new_part = Case.Case()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_case_stock(part_name)

        if part_category == "CPU":
            new_part = CPU.CPU()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_cpu_stock(part_name)

        if part_category == "MOTHERBOARDS":
            new_part = Motherboard.Motherboard()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_motherboard_stock(part_name)

        if part_category == "COOLING":
            new_part = cooling.Cooling()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_cooling_stock(part_name)

        if part_category == "MEMORY":
            new_part = Memory.Memory()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_memory_stock(part_name)

        if part_category == "GPU":
            new_part = GPU.GPU()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_gpu_stock(part_name)

        if part_category == "STORAGE":
            new_part = storage.Storage()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_storage_stock(part_name)

        if part_category == "POWER":
            new_part = Power_Supply.power_supply()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_power_stock(part_name)

        new_part_item = Item(new_part, part_name, total_price)
        print(new_part_item.get_item().get_info())
        cart_dict[new_part_item.get_id()] = new_part_item
        #add back cart_dict to db
        # print(cart_dict)
        db[current_user_id] = cart_dict
        db.close()

        inventory.set_available_cases()
        inventory.set_available_cpu()
        inventory.set_available_motherboards()
        inventory.set_available_cooling()
        inventory.set_available_memory()
        inventory.set_available_gpu()
        inventory.set_available_storage()
        inventory.set_available_power()
        inventory.set_available_opsys()

        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))


#creating a pc
@app.route('/dashboard/CreateAccessory/<path:part_category>/<path:part_name>/<path:part_price>', methods=["GET", "POST"])
@login_required
def create_accessory(part_category, part_name, part_price):
    if not(flask_login.current_user.get_role() == "ADMIN" or flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        return redirect(url_for('login'))
    if flask_login.current_user.get_role() == "ADMIN":
        return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
    # current_user_creating = UserModel.query.filter_by(email=current_user.get_email()).first()
    # current_user_id = current_user_creating.
    current_user_id = current_user.get_id()

    # update inventory available stock
    inventory.set_available_cases()
    inventory.set_available_cpu()
    inventory.set_available_motherboards()
    inventory.set_available_cooling()
    inventory.set_available_memory()
    inventory.set_available_gpu()
    inventory.set_available_storage()
    inventory.set_available_power()
    inventory.set_available_opsys()
    inventory.set_available_keyboards()
    inventory.set_available_mice()

    #initialize form with default options
    available_keyboards = inventory.get_available_keyboards()
    available_mice = inventory.get_available_mice()



    if request.method == "POST":
        # for each user, a dictionary is added as the key value, dictionary will add their PC
        cart_dict = {}
        db = shelve.open('carts.db', 'c')

        try:
            cart_dict = db[current_user_id]
        except:
            print("Error in retrieving carts from carts.db.")

        # #calculate price
        # total_price = pc_case.get_price + pc_motherboard.get_price() + pc_cpu.get_price() + pc_gpu.get_price() + pc_storage.get_price() + pc_cooling.get_price() + pc_power_supply.get_price() + pc_wifi.get_price() + pc_op_sys.get_price() + pc_memory.get_price()
        print(part_name)
        print(part_price)

        total_price = int(part_price)
        print(total_price)

        new_part = ""

        if part_category == "KEYBOARDS":
            new_part = Keyboard.Keyboard()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_keyboard_stock(part_name)

        if part_category == "MOUSE":
            new_part = Mouse.Mouse()
            new_part.set_name(part_name)
            new_part.set_price(total_price)
            inventory.decrement_mouse_stock(part_name)



        new_part_item = Item(new_part, part_name, total_price)
        print(new_part_item.get_item().get_info())
        cart_dict[new_part_item.get_id()] = new_part_item
        #add back cart_dict to db
        # print(cart_dict)
        db[current_user_id] = cart_dict
        db.close()

        inventory.set_available_keyboards()
        inventory.set_available_mice()


        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

@app.route('/dashboard/cart', methods=["GET", "POST"])
@login_required
def get_cart():
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))


    cart_dict = {}

    try:
        db = shelve.open('carts.db', 'r')
    except:
        db = shelve.open('carts.db', 'c')
        db.close()
        db = shelve.open('carts.db', 'r')

    try:
        cart_dict = db[current_user.get_id()]
        db.close()
    except:
        print("Error in retrieving carts from carts.db.")

    cart_list = []
    total = 0
    for key in cart_dict:
        item = cart_dict.get(key)
        cart_list.append(item)
        print(item.get_description())
        total += item.get_price()

    return render_template("seeCart.html", user=str(current_user.get_first_name()), count=len(cart_list), cart_list=cart_list, total_price=str(total))

@app.route('/dashboard/UpdatePC/<int:id>', methods=["GET", "POST"])
@login_required
def update_custom_pc(id):
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    # update inventory available stock
    inventory.set_available_cases()
    inventory.set_available_cpu()
    inventory.set_available_motherboards()
    inventory.set_available_cooling()
    inventory.set_available_memory()
    inventory.set_available_gpu()
    inventory.set_available_storage()
    inventory.set_available_power()
    inventory.set_available_opsys()
    inventory.set_available_keyboards()
    inventory.set_available_mice()

    # initialize form with default options
    available_cases = inventory.get_available_cases()
    available_cpu = inventory.get_available_cpu()
    available_motherboards = inventory.get_available_motherboards()
    available_cooling = inventory.get_available_cooling()
    available_memory = inventory.get_available_memory()
    available_gpu = inventory.get_available_gpu()
    available_storage = inventory.get_available_storage()
    available_power = inventory.get_available_power()
    available_opsys = inventory.get_available_opsys()

    print("Hey")
    print(available_motherboards)

    updatepcform = ConfigurePCForm(request.form, case=available_cases[0][0], motherboard=available_motherboards[0][0],
                                   cooling=available_cooling[0][0], memory=available_memory[0][0],
                                   gpu=available_gpu[0][0],
                                   primary_storage=available_storage[0][0],
                                   power_supply=available_power[0][0],
                                   op_sys=available_opsys[0][0])
    # print(updatepcform.case.choices)

    updatepcform.case.choices = available_cases
    updatepcform.cpu.choices = available_cpu
    updatepcform.motherboard.choices = available_motherboards
    updatepcform.cooling.choices = available_cooling
    updatepcform.memory.choices = available_memory
    updatepcform.gpu.choices = available_gpu
    updatepcform.primary_storage.choices = available_storage
    updatepcform.power_supply.choices = available_power
    updatepcform.op_sys.choices = available_opsys


    if request.method == 'POST' and updatepcform.validate():
        cart_dict = {}
        db = shelve.open('carts.db', 'w')
        try:
            cart_dict = db[current_user.get_id()]

        except:
            print("Error in retrieving carts from carts.db.")

        item = cart_dict.get(id)
        pc_obj = item.get_item()
        pc_description = updatepcform.description.data

        pc_case = updatepcform.case.data
        # pc_case_to_decrement = (pc_case, pc_case.split(",")[1])
        # print(pc_case_to_decrement)
        inventory.decrement_case_stock(pc_case.split(",")[1])
        # print(inventory.get_case_stock())

        pc_motherboard = updatepcform.motherboard.data
        inventory.decrement_motherboard_stock(pc_motherboard.split(",")[1])

        pc_cpu = updatepcform.cpu.data
        inventory.decrement_cpu_stock(pc_cpu.split(",")[1])

        pc_gpu = updatepcform.gpu.data
        inventory.decrement_gpu_stock(pc_gpu.split(",")[1])

        pc_storage = updatepcform.primary_storage.data
        inventory.decrement_storage_stock(pc_storage.split(",")[1])

        pc_cooling = updatepcform.cooling.data
        inventory.decrement_cooling_stock(pc_cooling.split(",")[1])

        pc_power_supply = updatepcform.power_supply.data
        inventory.decrement_power_stock(pc_power_supply.split(",")[1])

        pc_wifi = updatepcform.wifi_bluetooth.data

        pc_op_sys = updatepcform.op_sys.data
        inventory.decrement_opsys_stock(pc_op_sys.split(",")[1])

        pc_memory = updatepcform.memory.data
        inventory.decrement_memory_stock(pc_memory.split(",")[1])

        #calculate price
        total_price = int(pc_case.split(",")[0]) + int(pc_motherboard.split(",")[0]) + int(pc_cpu.split(",")[0]) + int(
            pc_storage.split(",")[0]) + int(pc_cooling.split(",")[0]) + int(pc_power_supply.split(",")[0]) + int(
            pc_wifi.split(",")[0]) + int(pc_op_sys.split(",")[0]) + int(pc_memory.split(",")[0])
        item.set_price(total_price)

        pc_obj.set_description(pc_description)
        item.set_description(pc_description)
        pc_obj.set_case(pc_case)
        pc_obj.set_motherboard(pc_motherboard)
        pc_obj.set_cpu(pc_cpu)
        pc_obj.set_gpu(pc_gpu)
        pc_obj.set_storage(pc_storage)
        pc_obj.set_cooling(pc_cooling)
        pc_obj.set_power_supply(pc_power_supply)
        pc_obj.set_wifi(pc_wifi)
        pc_obj.set_opsys(pc_op_sys)
        pc_obj.set_memory(pc_memory)



        db[current_user.get_id()] = cart_dict


        db.close()
        inventory.set_available_cases()
        inventory.set_available_cpu()
        inventory.set_available_motherboards()
        inventory.set_available_cooling()
        inventory.set_available_memory()
        inventory.set_available_gpu()
        inventory.set_available_storage()
        inventory.set_available_power()
        inventory.set_available_opsys()


        return redirect(url_for('get_cart',username=current_user.get_first_name(), logged_in=current_user.is_authenticated))
    else:
        cart_dict = {}
        db = shelve.open('carts.db', 'r')
        cart_dict = db[current_user.get_id()]


        item = cart_dict.get(id)
        pc_obj = item.get_item()
        print(pc_obj)
        updatepcform.description.data = pc_obj.get_description()

        updatepcform.case.data = pc_obj.get_case()
        # pc_case_to_increment = (pc_obj.get_case(), pc_obj.get_case().split(",")[1])
        # print(pc_case_to_increment)
        inventory.increment_case_stock(pc_obj.get_case().split(",")[1])
        # print(inventory.get_case_stock())

        updatepcform.motherboard.data = pc_obj.get_motherboard()
        inventory.increment_motherboard_stock(pc_obj.get_motherboard().split(",")[1])

        updatepcform.cpu.data = pc_obj.get_cpu()
        inventory.increment_cpu_stock(pc_obj.get_cpu().split(",")[1])

        updatepcform.gpu.data = pc_obj.get_gpu()
        inventory.increment_gpu_stock(pc_obj.get_gpu().split(",")[1])

        updatepcform.primary_storage.data = pc_obj.get_storage()
        inventory.increment_storage_stock(pc_obj.get_storage().split(",")[1])

        updatepcform.cooling.data = pc_obj.get_cooling()
        inventory.increment_cooling_stock(pc_obj.get_cooling().split(",")[1])

        updatepcform.power_supply.data = pc_obj.get_power_supply()
        inventory.increment_power_stock(pc_obj.get_power_supply().split(",")[1])

        updatepcform.wifi_bluetooth.data = pc_obj.get_wifi()

        updatepcform.op_sys.data = pc_obj.get_opsys()
        inventory.increment_opsys_stock(pc_obj.get_opsys().split(",")[1])

        updatepcform.memory.data = pc_obj.get_memory()
        inventory.increment_memory_stock(pc_obj.get_memory().split(",")[1])

        # print(pc_obj.get_case())
        # db[current_user.get_id()] = cart_dict
        db.close()
        inventory.set_available_cases()
        inventory.set_available_cpu()
        inventory.set_available_motherboards()
        inventory.set_available_cooling()
        inventory.set_available_memory()
        inventory.set_available_gpu()
        inventory.set_available_storage()
        inventory.set_available_power()
        inventory.set_available_opsys()

        return render_template('updatePC.html', form=updatepcform, logged_in=current_user.is_authenticated)


@app.route('/deleteItem/<int:id>', methods=["POST"])
@login_required
def delete_item(id):
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))
    cart_dict = {}
    db = shelve.open('carts.db', 'w')

    try:
        cart_dict = db[current_user.get_id()]
    except:
        print("Error in retrieving carts from carts.db.")

    print(cart_dict)

    #need to restock item if item is deleted
    item = cart_dict.pop(id)
    item_inside = item.get_item()
    if isinstance(item_inside, Computer):
        pc_case_to_increment = (item_inside.get_case(), item_inside.get_case().split(",")[1])
        inventory.increment_case_stock(item_inside.get_case().split(",")[1])
        inventory.increment_motherboard_stock(item_inside.get_motherboard().split(",")[1])
        inventory.increment_cpu_stock(item_inside.get_cpu().split(",")[1])
        inventory.increment_gpu_stock(item_inside.get_gpu().split(",")[1])
        inventory.increment_storage_stock(item_inside.get_storage().split(",")[1])
        inventory.increment_cooling_stock(item_inside.get_cooling().split(",")[1])
        inventory.increment_power_stock(item_inside.get_power_supply().split(",")[1])
        inventory.increment_opsys_stock(item_inside.get_opsys().split(",")[1])
        inventory.increment_memory_stock(item_inside.get_memory().split(",")[1])
        # print(inventory.get_case_stock())

        inventory.set_available_cases()
        inventory.set_available_cpu()
        inventory.set_available_motherboards()
        inventory.set_available_cooling()
        inventory.set_available_memory()
        inventory.set_available_gpu()
        inventory.set_available_storage()
        inventory.set_available_power()
        inventory.set_available_opsys()

    if isinstance(item_inside, Case.Case):
        inventory.increment_case_stock(item_inside.get_info())

        inventory.set_available_cases()

    if isinstance(item_inside, CPU.CPU):
        inventory.increment_cpu_stock(item_inside.get_info())
        inventory.set_available_cpu()

    if isinstance(item_inside, Motherboard.Motherboard):
        inventory.increment_motherboard_stock(item_inside.get_info())
        inventory.set_available_motherboards()

    if isinstance(item_inside, cooling.Cooling):
        inventory.increment_cooling_stock(item_inside.get_info())
        inventory.set_available_cooling()

    if isinstance(item_inside, Memory.Memory):
        inventory.increment_memory_stock(item_inside.get_info())
        inventory.set_available_memory()

    if isinstance(item_inside, GPU.GPU):
        inventory.increment_gpu_stock(item_inside.get_info())
        inventory.set_available_gpu()

    if isinstance(item_inside, storage.Storage):
        inventory.increment_storage_stock(item_inside.get_info())
        inventory.set_available_storage()

    if isinstance(item_inside, Power_Supply.power_supply):
        inventory.increment_power_stock(item_inside.get_info())
        inventory.set_available_power()

    if isinstance(item_inside, Keyboard.Keyboard):
        inventory.increment_keyboard_stock(item_inside.get_info())
        inventory.set_available_keyboards()

    if isinstance(item_inside, Mouse.Mouse):
        inventory.increment_mouse_stock(item_inside.get_info())
        inventory.set_available_mice()


    db[current_user.get_id()] = cart_dict
    db.close()

    return redirect(url_for('get_cart',username=current_user.get_first_name(), logged_in=current_user.is_authenticated))

######################################################################################################################################

















######################################################################################################################################
def _build_itemized_description_table(cart_dictionary):
    table_1 = Table(number_of_rows=len(list(cart_dictionary.keys()))+6, number_of_columns=5)
    for h in ["Serial Number", "Name", "Description", "Delivery Type", "Price"]:
        table_1.add(
            TableCell(
                Paragraph(h, font_color=X11Color("White")),
                background_color=HexColor("7986cb")
            )
        )

    odd_color = HexColor("BBBBBB")
    even_color = HexColor("FFFFFF")

    invoice_item_list = []

    name_list = []
    item_list = list(cart_dictionary.values())

    description_list = []
    delivery_type_list = []
    price_list = []

    pc_specs = ""
    for item in item_list:
        if is_PC(item):
            pc_specs_list = item.get_item().get_info()
            for part in pc_specs_list:
                pc_specs += part
            description_list.append(pc_specs)
        else:
            description_list.append(item.get_item().get_info())

        delivery_type_list.append(item.get_collection_type())
        price_list.append(item.get_price())
        name_list.append(item.get_description())

    # generate serial number
    N = 8
    serial_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

    invoice_item_tuple = []
    print(name_list)
    for key in name_list:
        N = 8
        serial_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        index_of_key = name_list.index(key)
        # make the tuple
        invoice_item_tuple.append(serial_code)
        invoice_item_tuple.append(key)
        invoice_item_tuple.append(description_list[index_of_key])
        invoice_item_tuple.append(delivery_type_list[index_of_key])
        invoice_item_tuple.append(price_list[index_of_key])

        # convert list to tuple
        invoice_item_tuple = tuple(invoice_item_tuple)

        # append tuple to item list
        invoice_item_list.append(invoice_item_tuple)

        # change tuple back to list to append
        invoice_item_tuple = []

    for item in invoice_item_list:
        c = even_color if invoice_item_list.index(item) % 2 == 0 else odd_color
        table_1.add(TableCell(Paragraph(str(item[0])), background_color=c))
        table_1.add(TableCell(Paragraph(str(item[1])), background_color=c))
        table_1.add(TableCell(Paragraph(str(item[2])), background_color=c))
        table_1.add(TableCell(Paragraph(str(item[3])), background_color=c))
        table_1.add(TableCell(Paragraph(str(item[4])), background_color=c))

    # add more rows just for design
    # for row_number in range(len(invoice_item_list), len(invoice_item_list) + 5):
    #     c = odd_color
    #     for _ in range(0, len(invoice_item_list)):
    #         table_1.add(TableCell(Paragraph(" "), background_color=c))
    #
    sub_total_price = 0
    for price in price_list:
        sub_total_price += price

    gst_amount = sub_total_price * (8/100)
    gst_amount = "{:.2f}".format(gst_amount)

    Voucher_code = "None Used"
    discount = 0

    total = sub_total_price + float(gst_amount) - discount
    total = "{:.2f}".format(total)

    table_1.add(TableCell(Paragraph("Subtotal", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=4))
    table_1.add(TableCell(Paragraph(str(sub_total_price), horizontal_alignment=Alignment.RIGHT)))
    table_1.add(TableCell(Paragraph("GST 8%", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=4))
    table_1.add(TableCell(Paragraph(gst_amount, horizontal_alignment=Alignment.RIGHT)))
    table_1.add(TableCell(Paragraph("Voucher Code", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=4))
    table_1.add(TableCell(Paragraph(str(Voucher_code), horizontal_alignment=Alignment.RIGHT)))
    table_1.add(TableCell(Paragraph("Discount", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=4))
    table_1.add(TableCell(Paragraph(str(discount), horizontal_alignment=Alignment.RIGHT)))
    table_1.add(TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=4))
    table_1.add(TableCell(Paragraph(str(total), horizontal_alignment=Alignment.RIGHT)))

    table_1.set_padding_on_all_cells(Decimal(2),Decimal(2),Decimal(2),Decimal(2),)
    table_1.no_borders()

    print("Itemized Table Success")
    return table_1

def _build_billing_info(user_model_obj):
    table_1 = Table(number_of_rows=6, number_of_columns=2)
    table_1.add(
        Paragraph(
            "Sold to Customer Details",
            background_color = HexColor("7986cb"),
            font_color = X11Color("White"),
        )
    )
    table_1.add(
        Paragraph(
            "Ship to Customer Details",
             background_color = HexColor("7986cb"),
             font_color = X11Color("White"),
        )
    )

    table_1.add(Paragraph("Medusa PCs")) # Full Name Sold To
    table_1.add(Paragraph(user_model_obj.get_first_name() + " " + user_model_obj.get_last_name())) # Full Name Ship To
    table_1.add(Paragraph("56 Accel Drive #08-01")) # Address Sold To
    table_1.add(Paragraph(user_model_obj.get_address())) # Address Ship To
    table_1.add(Paragraph("Singapore-657890")) # State and Zip Code Sold To
    table_1.add(Paragraph(user_model_obj.get_state() + "-" + user_model_obj.get_zip_code())) # State and Zip Code Ship To
    table_1.add(Paragraph("+65 65789045")) # Phone Sold To
    table_1.add(Paragraph(user_model_obj.get_phone())) # Phone Ship To
    table_1.add(Paragraph("Medusa Pte Ltd")) # Get Company Sold To
    table_1.add(Paragraph(user_model_obj.get_company())) # Get Company Ship To
    table_1.set_padding_on_all_cells(Decimal(2),Decimal(2),Decimal(2),Decimal(2),)
    table_1.no_borders()
    return table_1

def _build_invoice_information():
    table_1 = Table(number_of_rows=5, number_of_columns=3)

    table_1.add(Paragraph("56 Accel Drive #08-01"))
    table_1.add(Paragraph("Purchase Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    now = datetime.now()
    table_1.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))

    table_1.add(Paragraph("Singapore 657890"))
    table_1.add(Paragraph("Invoice #", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_1.add(Paragraph("%d" % (random.randint(10000000, 100000000))))

    warranty_expiry_date = pd.to_datetime(now) + pd.DateOffset(years=3)
    table_1.add(Paragraph("+65 65789045"))
    table_1.add(Paragraph("Warranty Expiry Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_1.add(Paragraph("%d/%d/%d" % (warranty_expiry_date.day, warranty_expiry_date.month, warranty_expiry_date.year)))

    table_1.add(Paragraph("medusapc123@gmail.com"))
    table_1.add(Paragraph(""))
    table_1.add(Paragraph(""))

    table_1.add(Paragraph("https://medusapc.com"))
    table_1.add(Paragraph(""))
    table_1.add(Paragraph(""))

    table_1.set_padding_on_all_cells(Decimal(2),Decimal(2),Decimal(2),Decimal(2),)
    table_1.no_borders()
    return table_1

# a shipment inherits from item class and contains the shipping rate id
def CreateShipment(item: Item):
    new_shipment = Shipment()
    new_shipment.set_item(item)
    return new_shipment


@app.route('/dashboard/checkout_finalise', methods=['GET','POST'])
@login_required
def remove_item_after_checkout():
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    cart_dict = {}

    # if successful need to add to cart
    db = shelve.open('carts.db', 'w')

    try:
        cart_dict = db[current_user.get_id()]
    except:
        print("Error in retrieving carts from carts.db.")

    # need to create another shelve to store transactions list
    transactions_dict = {}
    db_transactions = shelve.open('transactions.db', 'c')

    try:
        transactions_dict = db_transactions["Transactions"]
    except:
        print("Error in retrieving carts from transactions.db.")

    # need to create another shelve to store shipments list
    shipments_dict = {}
    db_shipments = shelve.open('Shipments.db', 'c')

    try:
        shipments_dict = db_shipments[current_user.get_id()]
    except:
        print("Error in retrieving shipments from Shipments.db.")

    # need to create another shelve to store universal shipments list
    universal_shipments_dict = {}
    db_universal_shipments = shelve.open('Universal_Shipments.db', 'c')

    try:
        universal_shipments_dict = db_universal_shipments["ALL_SHIPMENTS"]
    except:
        print("Error in retrieving all shipments from Universal_Shipments.db.")

    # adding to transactions dict and emptying cart dict
    item_list = []
    item_obj_list = []
    total = 0
    if request.args.get("delivery"):
        total += 50
    else:
        pass
    for key in cart_dict.keys():
        # tech_item = cart_dict[key].get_item()
        item_obj_list.append(cart_dict[key])
        item_list.append(cart_dict[key].get_description())
        total += cart_dict[key].get_price()

        current_date = datetime.now()

        ################################################################################
        # on successful checkout, need to open the transactions.db to create a shipment and add item to transactions.db

        transactions_dict[str(current_date) + ":" + str(key)] = cart_dict[key]  # retrieve Item obj to transactions_dict

        ################################################################################
        # on successful checkout, need to open the Shipments.db to create a shipment and add item to Shipments.db and Universal_Shipments.db

        # create shipment obj
        shipment_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        new_shipment = CreateShipment(cart_dict[key])
        new_shipment.set_id(shipment_id)
        new_shipment.set_shipping_status("Pending")
        new_shipment.set_order_date(current_date.date())

        # append the shipment obj into Shipments.db
        shipments_dict[shipment_id] = new_shipment
        universal_shipments_dict[shipment_id] = new_shipment

    # need to create user voucher database
    voucher_database = {}
    indi_user_vouchers = {} # dict to store all vouchers related to user

    try:
        db_user_vouchers = shelve.open('UserCoupons.db', "w")
    except:
        db_user_vouchers = shelve.open('UserCoupons.db', "c")

    try:
        voucher_database = db_user_vouchers["USER_VOUCHERS"]
    except:
        print("Unable to retrieve all user vouchers from UserCoupons.db")

    # check for voucher id
    voucher_id = request.args.get("voucher_id")

    if voucher_id not in indi_user_vouchers:
        pass
    else:
        # remove the used voucher database from the db
        indi_user_vouchers.pop(voucher_id)
        # remove the used voucher from stripe
        stripe.Coupon.delete(voucher_id)

    # update the database
    voucher_database[flask_login.current_user.get_id()] = indi_user_vouchers
    db_user_vouchers["USER_VOUCHERS"] = voucher_database




    db_user_vouchers.close()


    # increase the points of the current user's account
    # need to get current_user points balance
    points_Accounts = {}
    try:
        db_pointsAccounts = shelve.open('PointsAccounts.db', "w")
    except:
        db_pointsAccounts = shelve.open('PointsAccounts.db', "c")

    try:
        points_Accounts = db_pointsAccounts["Points_Accounts"]
    except:
        print("Unable to retrieve Points Accounts from PointsAccounts.db")
    print(points_Accounts)

    user_account = points_Accounts[flask_login.current_user.get_id()]
    current_points = user_account.get_points()
    user_account.set_points(current_points + (total // 5))

    db_pointsAccounts["Points_Accounts"] = points_Accounts


    db_transactions["Transactions"] = transactions_dict
    db_shipments[current_user.get_id()] = shipments_dict
    db_universal_shipments["ALL_SHIPMENTS"] = universal_shipments_dict
    db[current_user.get_id()] = {}

    db_pointsAccounts.close()

    db_transactions.close()
    db_shipments.close()
    db_universal_shipments.close()
    db.close()

    # Create invoice
    pdf = Document()

    # add page
    page = Page()
    pdf.add_page(page)

    # page layout
    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)

    page_layout.add(
        Image(
            "https://static.vecteezy.com/system/resources/previews/007/741/295/original/medusa-logo-natural-beautiful-woman-s-face-snakes-line-art-logo-for-beauty-salon-free-vector.jpg",
            width=Decimal(220),
            height=Decimal(192))
    )

    # Invoice Information table
    page_layout.add(_build_invoice_information())

    # add empty paragraph for spacing
    page_layout.add(Paragraph(""))

    # billing info
    user_obj = current_user
    page_layout.add(_build_billing_info(user_obj))

    # add empty paragraph for spacing
    page_layout.add(Paragraph(""))
    #
    # #add item description
    page_layout.add(_build_itemized_description_table(cart_dict))

    # add outline
    pdf.add_outline("invoice", 0, DestinationType.FIT, page_nr=0)

    # build pdf
    with open("invoice.pdf", "wb") as pdf_to_generate:
        PDF.dumps(pdf_to_generate, pdf)




    #once done return to cart page
    print("Finalised")
    return redirect(url_for('get_cart',username=current_user.get_first_name(), logged_in=current_user.is_authenticated))

@app.route('/checkout', methods=["POST"])
@login_required
def checkout():
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    # this portion of data must be posted to the metadata of the successful checkout
    createshippingdate = CreateShippingDate(request.form)
    collectiontype = createshippingdate.collection_type.data
    shippingdate = createshippingdate.shipping_date.data
    shippingtime = createshippingdate.shipping_time.data
    destinationaddress = createshippingdate.destination_address.data
    voucher_id = createshippingdate.voucher_form.data

    print(stripe.Coupon.list(limit=5))

    cart_dict = {}
    db = shelve.open('carts.db', 'w')

    try:
        cart_dict = db[current_user.get_id()]
    except:
        print("Error in retrieving carts from carts.db.")



    #need to create another shelve to store transactions list
    transactions_dict = {}
    db_transactions = shelve.open('transactions.db', 'c')

    try:
        transactions_dict = db_transactions["Transactions"]
    except:
        print("Error in retrieving carts from transactions.db.")

    # add to item_obj_list from cart

    # #adding to transactions dict and emptying cart dict
    #
    item_list = []
    item_obj_list = []
    total = 0
    for key in cart_dict.keys():
        # tech_item = cart_dict[key].get_item()
        item_obj_list.append(cart_dict[key])
        item_list.append(cart_dict[key].get_description())
        total += cart_dict[key].get_price()

        current_date = datetime.now()
        cart_dict[key].set_collection_type(collectiontype)
        cart_dict[key].set_shipping_date(shippingdate)
        cart_dict[key].set_shipping_time(shippingtime)
        cart_dict[key].set_destination_address(destinationaddress)
        cart_dict[key].set_owner(current_user.get_first_name())
        # transactions_dict[str(current_date) +":" + str(key)] = cart_dict[key] #retrieve Item obj to transactions_dict
    #
    # db_transactions["Transactions"] = transactions_dict
    #
    db[current_user.get_id()] = cart_dict
    db_transactions.close()
    db.close()
    #
    # # Create invoice
    # pdf = Document()
    #
    # # add page
    # page = Page()
    # pdf.add_page(page)
    #
    # # page layout
    # page_layout = SingleColumnLayout(page)
    # page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
    #
    # page_layout.add(
    #     Image("https://static.vecteezy.com/system/resources/previews/007/741/295/original/medusa-logo-natural-beautiful-woman-s-face-snakes-line-art-logo-for-beauty-salon-free-vector.jpg",
    #           width=Decimal(220),
    #           height=Decimal(192))
    # )
    #
    # # Invoice Information table
    # page_layout.add(_build_invoice_information())
    #
    # # add empty paragraph for spacing
    # page_layout.add(Paragraph(""))
    #
    # # billing info
    # user_obj = current_user
    # page_layout.add(_build_billing_info(user_obj))
    #
    # # add empty paragraph for spacing
    # page_layout.add(Paragraph(""))
    # #
    # # #add item description
    # page_layout.add(_build_itemized_description_table(cart_dict))
    #
    # # add outline
    # pdf.add_outline("invoice", 0, DestinationType.FIT, page_nr=0)
    #
    # # build pdf
    # with open("invoice.pdf", "wb") as pdf_to_generate:
    #     PDF.dumps(pdf_to_generate, pdf)







    # need a list that contains multiple dicts for checkout session
    line_items_list = []
    line_items_element = {
        "price": None,
        "quantity": None
    }

    for item in item_obj_list:
        # item = item.get_item()

        # creating a product obj
        new_item = None
        # stripe.Product.create(name=item.get_description(), id=item.get_description().replace(" ", ""))
        try:
            new_item = stripe.Product.create(name=item.get_description(), id=item.get_description().replace(" ", ""))
        except:
            new_item = stripe.Product.retrieve(item.get_description().replace(" ", ""))
            print(new_item)
        # creating a price obj to attach to product obj

        print(new_item["id"])

        price = stripe.Price.create(
            unit_amount = item.get_price() * 100, # in cents
            currency="sgd",
            product=new_item["id"]
        )

        price_value = stripe.Price.retrieve(price["id"])

        line_items_element_copy = line_items_element.copy()
        line_items_element_copy["price"] = price_value["id"]
        line_items_element_copy["quantity"] = 1
        line_items_list.append(line_items_element_copy)
        print("Line Item element")



    # create the shipping options if it has not been created
    shipping_options_dict = {}
    try:
        shipping_options_dict = shelve.open("Shipping_Rates.db", "r")["Shipping_Rates"]
    except:
        CreateShippingRate()
        shipping_options_dict = shelve.open("Shipping_Rates.db", "r")["Shipping_Rates"]

    print(shipping_options_dict)

    # need to apply voucher if valid voucher id is found
    # need to create user voucher database
    voucher_database = {}
    indi_user_vouchers = {} # dict to store all vouchers related to user

    try:
        db_user_vouchers = shelve.open('UserCoupons.db', "r")
    except:
        db_user_vouchers = shelve.open('UserCoupons.db', "c")

    try:
        voucher_database = db_user_vouchers["USER_VOUCHERS"]
    except:
        print("Unable to retrieve all user vouchers from UserCoupons.db")
    print(voucher_database)
    print(flask_login.current_user.get_id())
    print(voucher_database[flask_login.current_user.get_id()])
    # check for the voucher id
    voucher_to_use = None
    indi_user_vouchers = voucher_database[flask_login.current_user.get_id()]
    print("Checkout")
    print(voucher_database)
    print(indi_user_vouchers)
    if voucher_id in list(indi_user_vouchers.keys()):
        voucher_to_use = stripe.Coupon.retrieve(voucher_id)
        print("Voucher retrieved")
    else:
        pass

    voucher_use_dict = {}
    if voucher_to_use == None:
        discount_array = []
    else:
        voucher_use_dict['coupon'] = voucher_to_use["id"]
        discount_array = []
        discount_array.append(voucher_use_dict)

    print("Hello")
    print(discount_array)

    db_user_vouchers.close()


    if collectiontype == "Delivery":
        # need to create a checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types= ["card", "alipay", "grabpay", "paynow"],
                shipping_options=[{"shipping_rate": shipping_options_dict["Delivery"]}],
                shipping_address_collection={"allowed_countries": ["SG", "US", "CA"]},
                line_items=line_items_list,

                mode='payment',
                discounts=discount_array,

                success_url= f"http://127.0.0.1:5000/dashboard/checkout_finalise?username={current_user.get_first_name()}&logged_in=True&delivery=True&voucher_id={voucher_id}",
                cancel_url= f"http://127.0.0.1:5000/dashboard/cart?username={current_user.get_first_name()}&logged_in=True&voucher_id={voucher_id}",

            )
        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)
    else:
        # need to create a checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card", "alipay", "grabpay", "paynow"],
                shipping_options=[{"shipping_rate": shipping_options_dict["Self-Collection"]}],
                shipping_address_collection={"allowed_countries": ["SG", "US", "CA"]},
                line_items=line_items_list,
                mode='payment',
                discounts=discount_array,

                success_url= f"http://127.0.0.1:5000/dashboard/checkout_finalise?username={current_user.get_first_name()}&logged_in=True&delivery=False&voucher_id={voucher_id}",
                cancel_url= f"http://127.0.0.1:5000/dashboard/cart?username={current_user.get_first_name()}&logged_in=True&voucher_id={voucher_id}",

            )
        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)


#############################################################################################################################

#generate admin user
@app.route('/createAdminUser', methods=["GET"])
def createAdminUser():
    if request.method == "GET":
        # users_dict = {}
        # db = shelve.open('user.db', 'c')
        #
        # try:
        #     users_dict = db['Users']
        # except:
        #     print("Error in retrieving Users from user.db.")

        #hashing, salting and storing the password
        password = "Admin1"
        password = password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)
        # new_user = User.User(createuserform.first_name.data,
        #                  createuserform.last_name.data,
        #                  createuserform.email.data,
        #                  bcrypt_hash
        # )
        # users_dict[new_user.get_user_id()] = users_dict
        # db['Users'] = users_dict
        # db.close()

        new_user = Admin(first_name="Admin1",
                             last_name="Admin1",
                             email="Admin1@gmail.com",
                             password=bcrypt_hash,
                             address="56 Accel Drive #08-01",
                             country="Singapore",
                             state="Singapore",
                             zip_code="657890",
                             company="Medusa Pte Ltd",
                             phone="+65 65789045",
                             role="ADMIN",
                             )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))

# create an admin user

#special admin login page
@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    createloginform = CreateLoginForm(request.form)
    # if request.method == "POST" and createloginform.validate():
    #     users_dict = {}
    #     db = shelve.open('user.db', 'r')
    #
    #     try:
    #         users_dict = db['Users']
    #         email = createloginform.email.data
    #         password = createloginform.password.data
    #         password = password.encode('utf-8')
    #         b64pwd = b64encode(SHA256.new(password).digest())
    #         user = users_dict.
    #     except:
    #         print("Error in retrieving Users from user.db.")


    if request.method == "POST" and createloginform.validate():
        email = createloginform.email.data
        password = createloginform.password.data
        password = password.encode('utf-8')
        b64pwd = b64encode(SHA256.new(password).digest())

        user_in_db = UserModel.query.filter_by(email=email).first()
        admin_ids = Admin.query.all()
        user_id = user_in_db.get_id()
        admin_id_list = []
        for admin in admin_ids:
            admin_id_list.append(admin.id)

        if not user_in_db:
            flash("That email does not exist, please try again or register for an account")
            return redirect(url_for('admin_login'))
        elif int(user_id) not in admin_id_list:
            flash("That email is not a registered admin user, please try again or register for an account")
            print("Unsuccessful")

        elif not valid_password(b64pwd, user_in_db.password):
            flash("Password Incorrect, please try again")
            return redirect(url_for('admin_login'))
        else:
            login_user(user_in_db)
            print("Success")
            return redirect(url_for('get_admin_dashboard', username=user_in_db.get_first_name()))
    return render_template("admin_login.html",form=createloginform, logged_in=current_user.is_authenticated)

def create_graph(dictionary):
    product_dict = dictionary
    # print(product_dict)
    s = pd.Series(data=product_dict, index=product_dict.keys())
    fig, ax = plt.subplots()

    s.plot.barh()

    fig.savefig('static/media/plot.png', bbox_inches='tight')

#admin dashboard
@app.route('/dashboard_admin/<path:username>')
@login_required
def get_admin_dashboard(username):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))
    current_user = username
    print(type(current_user))

    transactions_dict = {}
    transactions_list = []
    time_transactions_dict = {}
    key_list = []

    #to make line chart
    product_list = ["Intel Tier 1", "Intel Tier 2", "Intel Tier 3"]
    product_dict_count  = {
        "Intel Tier 1": 0,
        "Intel Tier 2": 0,
        "Intel Tier 3": 0
    }
    revenue = 0
    # try:
    with shelve.open('transactions.db', 'r') as db_transactions:
        transactions_dict = db_transactions["Transactions"]

        key_list = transactions_dict.keys()

        for key in transactions_dict:
            item = transactions_dict.get(key)
            transactions_list.append(item)
            revenue += item.get_price()

            #this dict will contain all items
            time_transactions_dict[key] = item
            if item.get_description() in product_dict_count:
                product_dict_count[item.get_description()] += 1
            else:
                product_dict_count[item.get_description()] = 0
                product_dict_count[item.get_description()] += 1

        # print(product_dict_count)


        p = multiprocessing.Process(target=create_graph, args=(product_dict_count,))
        p.start()


    # except:
    #     # db_transactions = shelve.open('transactions.db', 'c')
    #     print("Unable to retrieve transactions")




    return render_template("dashboard_admin.html", user=str(current_user), count=len(transactions_list), time_transactions_dict=time_transactions_dict,  total_revenue = revenue)


@app.route('/export_transactions', methods=['GET', 'POST'])
@login_required
def export_transactions():
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))
    transactions_dict = {}
    transactions_list = []
    item_list = []
    parts_list = []
    accessories_list = []
    parts_price_list = []
    accessories_price_list = []
    time_transactions_dict = {}
    excel_transactions = {}
    excel_parts_transaction = {}
    excel_accessories_transaction = {}
    key_list = []
    parts_key_list = []
    accessories_key_list = []

    #part list
    case_list = []
    motherboard_list = []
    cpu_list = []
    gpu_list = []
    storage_list = []
    cooling_list = []
    power_supply_list = []
    wifi_list = []
    op_sys_list = []
    memory_list = []

    #accessories list
    keyboards_list = []
    mice_accessories_list = []

    #buyer list
    pc_buyer_list = []
    parts_buyer_list = []
    accessories_buyer_list = []

    #time shipping
    pc_shipping_time = []
    parts_shipping_time = []
    accessories_shipping_time = []

    revenue = 0
    try:
        with shelve.open('transactions.db', 'r') as db_transactions:
            transactions_dict = db_transactions["Transactions"]
            print(transactions_dict)

            key_list = []

            for key in transactions_dict:
                item = transactions_dict.get(key)
                if isinstance(item.get_item(), Computer):
                    key_list.append(key)
                    pc_buyer_list.append(item.get_owner())
                    pc_shipping_time.append(item.get_shipping_time())
                elif isinstance(item.get_item(), Keyboard.Keyboard):
                    accessories_key_list.append(key)
                    accessories_buyer_list.append(item.get_owner())
                    accessories_shipping_time.append(item.get_shipping_time())
                elif isinstance(item.get_item(), Mouse.Mouse):
                    accessories_key_list.append(key)
                    accessories_buyer_list.append(item.get_owner())
                    accessories_shipping_time.append(item.get_shipping_time())
                else:
                    parts_key_list.append(key)
                    parts_buyer_list.append(item.get_owner())
                    parts_shipping_time.append(item.get_shipping_time())
                transactions_list.append(item)
                revenue += item.get_price()
                time_transactions_dict[key] = item

                if isinstance(item.get_item(), Computer):
                    #need to add to parts list
                    case_list.append(item.get_item().get_case().split(",")[1])
                    motherboard_list.append(item.get_item().get_motherboard().split(",")[1])
                    cpu_list.append(item.get_item().get_cpu().split(",")[1])
                    gpu_list.append(item.get_item().get_gpu().split(",")[1])
                    storage_list.append(item.get_item().get_storage().split(",")[1])
                    cooling_list.append(item.get_item().get_cooling().split(",")[1])
                    power_supply_list.append(item.get_item().get_power_supply().split(",")[1])
                    wifi_list.append(item.get_item().get_wifi().split(",")[1])
                    op_sys_list.append(item.get_item().get_opsys().split(",")[1])
                    memory_list.append(item.get_item().get_memory().split(",")[1])

                    # print(item.get_item().get_case().split(",")[1])
                    # print(item.get_item().get_motherboard().split(",")[1])
                    # print(item.get_item().get_cpu().split(",")[1])
                    # print(item.get_item().get_gpu().split(",")[1])
                    # print(item.get_item().get_storage().split(",")[1])
                    # print(item.get_item().get_cooling().split(",")[1])
                    # print(item.get_item().get_power_supply().split(",")[1])
                    # print(item.get_item().get_wifi().split(",")[1])
                    # print(item.get_item().get_opsys().split(",")[1])
                    # print(item.get_item().get_memory().split(",")[1])

                    # excel_transactions[key] = item.get_description()
                    item_list.append(item.get_description())
                elif isinstance(item.get_item(), Keyboard.Keyboard):
                    accessories_list.append(item.get_item().get_info())
                    accessories_price_list.append(item.get_item().get_price())
                elif isinstance(item.get_item(), Mouse.Mouse):
                    accessories_list.append(item.get_item().get_info())
                    accessories_price_list.append(item.get_item().get_price())
                else:
                    parts_list.append(item.get_item().get_info())
                    parts_price_list.append(item.get_item().get_price())


            excel_transactions['Timestamp'] = key_list
            excel_transactions['Items'] = item_list
            excel_transactions['Case'] = case_list
            excel_transactions['Motherboard'] = motherboard_list
            excel_transactions['CPU'] = cpu_list
            excel_transactions['GPU'] = gpu_list
            excel_transactions['Storage'] = storage_list
            excel_transactions['Cooling'] = cooling_list
            excel_transactions['Power Supply'] = power_supply_list
            excel_transactions['Wifi'] = wifi_list
            excel_transactions['Operating System'] = op_sys_list
            excel_transactions['Memory'] = memory_list
            excel_transactions['Buyer'] = pc_buyer_list
            excel_transactions['Shipping time chosen'] = pc_shipping_time

            excel_parts_transaction['Timestamp'] = parts_key_list
            excel_parts_transaction['Item'] = parts_list
            excel_parts_transaction['Price'] = parts_price_list
            excel_parts_transaction['Buyer'] = parts_buyer_list
            excel_parts_transaction['Shipping time chosen'] = parts_shipping_time

            excel_accessories_transaction['Timestamp'] = accessories_key_list
            excel_accessories_transaction['Item'] = accessories_list
            excel_accessories_transaction['Price'] = accessories_price_list
            excel_accessories_transaction['Buyer'] = accessories_buyer_list
            excel_accessories_transaction['Shipping time chosen'] = accessories_shipping_time

            # print("Here")
            # print(excel_transactions)
            # using pandas to make a dataframe
            transaction_df = pd.DataFrame(excel_transactions)
            parts_transaction_df = pd.DataFrame(excel_parts_transaction)
            accessories_transaction_df = pd.DataFrame(excel_accessories_transaction)
            # dump dataframe to excel sheet
            writer_device = pd.ExcelWriter('reports/transaction_report.xlsx', engine='xlsxwriter')
            transaction_df.to_excel(writer_device, sheet_name='Sheet1', startrow=3)
            parts_transaction_df.to_excel(writer_device, sheet_name='Sheet2', startrow=3)
            accessories_transaction_df.to_excel(writer_device, sheet_name='Sheet3', startrow=3)

            # get book and sheet obj for further manipulation
            book = writer_device.book
            sheet = writer_device.sheets['Sheet1']
            sheet2 = writer_device.sheets['Sheet2']
            sheet3 = writer_device.sheets['Sheet3']

            # add title to report
            bold = book.add_format({'bold': True, 'size': 24})
            title = datetime.now().date()
            sheet.write('A2', 'Transaction Report For PC' + str(title), bold)
            sheet2.write('A2', 'Transaction Report For PC Parts' + str(title), bold)
            sheet3.write('A2', 'Transaction Report For PC Accessories' + str(title), bold)

            writer_device.save()

            print("Successful report generation")


    except Exception as e:
        # print("Unable to retrieve transactions")
        print(e)

    return redirect(url_for('get_admin_dashboard', username=current_user.get_first_name()))



######################################################################################################################
# INVENTORY MANAGEMENT

@app.route('/inventory_management', methods=['GET', 'POST'])
@login_required
def manageInventory():
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    createproductform = CreateProductForm(request.form)
    try:
        db = shelve.open('inventory.db', "r")
    except:
        inventory.create_inventory()
    db.close()

    return render_template("manageInventory.html", username=flask_login.current_user.get_first_name(), user=flask_login.current_user.get_first_name(), inventory=inventory, form=createproductform)

@app.route('/dashboard_admin/<path:username>/add_item', methods=['GET', 'POST'])
@login_required
def create_product(username):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username
    createproductform = CreateProductForm(request.form)


    if request.method == "POST":
        product = []
        product_price = f"{createproductform.price.data},{createproductform.name.data}"
        product.append(product_price)
        product.append(createproductform.name.data)
        tuple(product)

        products_dict = {}
        products_db = shelve.open('products.db', 'w')

        try:
            products_dict = products_db["PRODUCTS"]
        except:
            print("Error in retrieving products from products.db")

        products_dict[createproductform.category.data].append(product)

        products_db["PRODUCTS"] = products_dict
        products_db.close()

        inventory.update_inventory()

        # need to add new product stock
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db.")

        category = createproductform.category.data
        inventory_category_dict = inventory_dict[category]
        inventory_category_dict[createproductform.name.data] = 10

        if createproductform.category.data == "CASES":
            inventory.set_available_cases()
        elif createproductform.category.data == "CPU":
            inventory.set_available_cpu()
        elif createproductform.category.data == "MOTHERBOARDS":
            inventory.set_available_motherboards()
        elif createproductform.category.data == "COOLING":
            inventory.set_available_cooling()
        elif createproductform.category.data == "MEMORY":
            inventory.set_available_memory()
        elif createproductform.category.data == "GPU":
            inventory.set_available_gpu()
        elif createproductform.category.data == "STORAGE":
            inventory.set_available_storage()
        elif createproductform.category.data == "POWER":
            inventory.set_available_power()
        elif createproductform.category.data == "OPSYS":
            inventory.set_available_opsys()
        elif createproductform.category.data == "KEYBOARDS":
            inventory.set_available_keyboards()
        elif createproductform.category.data == "MOUSE":
            inventory.set_available_mice()


        db["INVENTORY"] = inventory_dict
        db.close()

        inventory.update_inventory()
        inventory.update_products()


        return redirect(url_for('manageInventory', username=flask_login.current_user.get_first_name()))

@app.route('/dashboard_admin/<path:username>/delete_item/<path:item_type>/<path:product_name>/<path:price>', methods=['GET','POST'])
@login_required
def delete_product(username, item_type, product_name, price):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    products_dict = {}
    try:
        products_db = shelve.open("products.db", "w")
    except:
        products_db = shelve.open("products.db", "c")

    try:
        products_dict = products_db["PRODUCTS"]
    except:
        print("Could not retrieve products from products.db.")

    print(products_dict)
    product_key_listed = []

    product_key = f"{price},{product_name}"
    product_key_listed.append(product_key)
    product_key_listed.append(product_name)
    print(product_key_listed)
    index_to_delete = products_dict[item_type].index(product_key_listed)
    products_dict[item_type].pop(index_to_delete)

    products_db["PRODUCTS"] = products_dict

    inventory_dict = {}
    try:
        inventory_db = shelve.open("inventory.db", "w")
    except:
        inventory_db = shelve.open("inventory.db", "c")

    try:
        inventory_dict = inventory_db["INVENTORY"]
    except:
        print("Could not retrieve inventory from inventory.db.")

    inventory_dict[item_type].pop(product_name)

    inventory_db["INVENTORY"] = inventory_dict

    products_db.close()
    inventory_db.close()



    if item_type == "CASES":
        inventory.set_available_cases()
    elif item_type == "CPU":
        inventory.set_available_cpu()
    elif item_type == "MOTHERBOARDS":
        inventory.set_available_motherboards()
    elif item_type == "COOLING":
        inventory.set_available_cooling()
    elif item_type == "MEMORY":
        inventory.set_available_memory()
    elif item_type == "GPU":
        inventory.set_available_gpu()
    elif item_type == "STORAGE":
        inventory.set_available_storage()
    elif item_type == "POWER":
        inventory.set_available_power()
    elif item_type == "OPSYS":
        inventory.set_available_opsys()
    elif item_type == "KEYBOARDS":
        inventory.set_available_keyboards()
    elif item_type == "MOUSE":
        inventory.set_available_mice()

    inventory.update_inventory()
    inventory.update_products()
    print(inventory.get_case_stock())

    return redirect(url_for('manageInventory', username=flask_login.current_user.get_first_name()))



@app.route('/add_inventory/<path:item_type>/<path:item_id>', methods=['POST'])
@login_required
def addInventory(item_type, item_id):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    if request.method == "POST":
        inventory_dict = {}
        db = shelve.open('inventory.db', 'w')

        try:
            inventory_dict = db["INVENTORY"]
        except:
            print("Error in retrieving inventory from inventory.db")

        # print(request.form.get('num'))
        print(item_id)
        number_to_add = request.form.get('num')
        print(number_to_add)
        inventory_dict[item_type][item_id] += int(number_to_add)
        print("Inventory")
        print(inventory_dict)
        db["INVENTORY"] = inventory_dict
        db.close()

        inventory.update_inventory()
        inventory.set_available_cases()
        inventory.set_available_cpu()
        inventory.set_available_motherboards()
        inventory.set_available_cooling()
        inventory.set_available_memory()
        inventory.set_available_gpu()
        inventory.set_available_storage()
        inventory.set_available_power()
        inventory.set_available_opsys()



        return redirect(url_for('manageInventory', username=current_user.get_first_name()))

########################################################################
#error handler
    # @app.route('')
########################################################################


# Pricelist

@app.route("/pricelist_download", methods=['GET', 'POST'])
def pricelist_download():
    if not(flask_login.current_user.get_role() == "GUEST" or flask_login.current_user.get_role() == "USER"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))
    if request.method == "POST":
        return send_file("pricelist.txt", as_attachment=True)
    return render_template("customer_download_pricelist.html", user=flask_login.current_user.get_first_name(), logged_in=current_user.is_authenticated )

@app.route("/pricelist_upload", methods=['GET', 'POST'])
def pricelist_upload():
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', user=flask_login.current_user.get_first_name(), logged_in=current_user.is_authenticated))
    if request.method == "POST":
        file = request.files['pricelist']
        file.save("pricelist.txt")
        print("Save success")
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    return render_template("admin_upload_pricelist.html", username=flask_login.current_user.get_first_name(), user=flask_login.current_user.get_first_name())

###################################################################################
# Shipping rates

def CreateShippingRate():
    self_collection = stripe.ShippingRate.create(
        display_name = "Self-Collection",
        type = "fixed_amount",
        fixed_amount={
            'amount': 0,
            'currency': 'sgd',
        },
        delivery_estimate={
            'minimum': {
                'unit': 'business_day',
                'value': 5,
            },
            'maximum': {
                'unit': 'business_day',
                'value': 7
            },
        }
    )
    Delivery = stripe.ShippingRate.create(
        display_name = "Delivery",
        type = "fixed_amount",
        fixed_amount={
            'amount': 50*100,
            'currency': 'sgd',
        },
        delivery_estimate={
            'minimum': {
                'unit': 'business_day',
                'value': 5,
            },
            'maximum': {
                'unit': 'business_day',
                'value': 7
            },
        }
    )

    db = shelve.open("Shipping_Rates.db", "c")

    Shipping_Rates = {}
    Shipping_Rates["Self-Collection"] = self_collection["id"]
    Shipping_Rates["Delivery"] = Delivery["id"]


    db["Shipping_Rates"] = Shipping_Rates

    db.close()



# route to view all user shipments
@app.route("/dashboard/orders/<path:username>", methods=['GET', 'POST'])
@login_required
def view_user_shipments(username):
    if not(flask_login.current_user.get_role() == "GUEST" or flask_login.current_user.get_role() == "USER"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username
    shipments_dict = {}
    try:
        db = shelve.open('Universal_Shipments.db', "r")
        shipments_dict = db["ALL_SHIPMENTS"]
    except:
        db = shelve.open('Universal_Shipments.db', "c")

    db.close()

    return render_template('viewUserShipments.html', user=str(current_user), username=flask_login.current_user.get_first_name(), logged_in=flask_login.current_user.is_authenticated, shipments_dict=shipments_dict)


# route for admin to view all user shipments
@app.route("/dashboard_admin/<path:username>/shipments", methods=['GET', 'POST'])
@login_required
def admin_view_user_shipments(username):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    #this dictionary contains a dictionary of subdictionaries each representing user orders
    universal_shipments_dict = {}
    try:
        db = shelve.open('Universal_Shipments.db', "r")

    except:
        db = shelve.open('Universal_Shipments.db', "c")

    try:
        universal_shipments_dict = db["ALL_SHIPMENTS"]
    except:
        print("Could not retrieve All Shipments from Universal_Shipments.db")

    db.close()

    return render_template('viewAdminShipments.html', user=str(current_user), username=flask_login.current_user.get_first_name(), logged_in=flask_login.current_user.is_authenticated, shipments_dict=universal_shipments_dict)


# route to update shipping status
@app.route("/dashboard_admin/<path:username>/shipments/update_status/<path:item_id>", methods=['GET', 'POST'])
@login_required
def admin_update_user_shipments(username, item_id):

    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    new_status = request.form.get("statuses")
    print("New status")
    print(new_status)

    universal_shipments_dict = {}
    try:
        db = shelve.open('Universal_Shipments.db', "w")

    except:
        db = shelve.open('Universal_Shipments.db', "c")

    try:
        universal_shipments_dict = db["ALL_SHIPMENTS"]
    except:
        print("Could not retrieve All Shipments from Universal_Shipments.db")


    universal_shipments_dict[item_id].set_shipping_status(new_status)




    db["ALL_SHIPMENTS"] = universal_shipments_dict

    db.close()



    return redirect(url_for('admin_view_user_shipments', user=str(current_user), username=flask_login.current_user.get_first_name(), logged_in=flask_login.current_user.is_authenticated))

# route to delete shipment from view
# route to update shipping status
@app.route("/dashboard_admin/<path:username>/shipments/delete_shipment/<path:item_id>", methods=['GET', 'POST'])
@login_required
def admin_delete_user_shipments(username, item_id):

    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    universal_shipments_dict = {}
    try:
        db = shelve.open('Universal_Shipments.db', "w")

    except:
        db = shelve.open('Universal_Shipments.db', "c")

    try:
        universal_shipments_dict = db["ALL_SHIPMENTS"]
    except:
        print("Could not retrieve All Shipments from Universal_Shipments.db")

    universal_shipments_dict.pop(item_id)

    db["ALL_SHIPMENTS"] = universal_shipments_dict

    db.close()

    return redirect(
        url_for('admin_view_user_shipments', user=str(current_user), username=flask_login.current_user.get_first_name(),
                logged_in=flask_login.current_user.is_authenticated))


##################################################################################################################################################

# will store the id of these coupons in Coupons.db
def create_coupon(discount_type, value, number_of_redeems):
    new_coupon = stripe.Coupon.create(
        amount_off = value * 100,
        duration="once",
        max_redemptions=number_of_redeems
    )

def retrieve_coupons(id):
    return stripe.Coupon.retrieve(id)


def delete_coupon(id):
    stripe.Coupon.delete(id)
    return "Success"



# REWARDS SYSTEM

@app.route("/dashboard_admin/<path:username>/discount_codes/delete/<path:coupon_id>", methods=['GET', 'POST'])
@login_required
def delete_discount_code(username, coupon_id):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    if request.method == "POST":

        coupons_dict = {}

        try:
            db = shelve.open('CustomerCoupons.db', "w")
        except:
            db = shelve.open('CustomerCoupons.db', "c")

        try:
            coupons_dict = db["COUPONS"]
        except:
            print("Unable to retrieve Coupons from coupons.db.")

        coupons_dict.pop(coupon_id)

        db["COUPONS"] = coupons_dict

        db.close()




    return redirect(url_for('admin_view_promo_code', user=str(current_user), username=flask_login.current_user.get_first_name(),
            logged_in=flask_login.current_user.is_authenticated))



@app.route("/dashboard_admin/<path:username>/discount_codes/update/<path:coupon_id>", methods=['GET', 'POST'])
@login_required
def update_discount_code(username, coupon_id):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    if request.method == "POST":

        coupons_dict = {}

        try:
            db = shelve.open('CustomerCoupons.db', "w")
        except:
            db = shelve.open('CustomerCoupons.db', "c")

        try:
            coupons_dict = db["COUPONS"]
        except:
            print("Unable to retrieve Coupons from coupons.db.")

        new_status = request.form.get("statuses")
        if new_status == "Active":
            coupons_dict[coupon_id].set_status_to_active()
        else:
            coupons_dict[coupon_id].set_status_to_expired()

        db["COUPONS"] = coupons_dict

        db.close()




    return redirect(url_for('admin_view_promo_code', user=str(current_user), username=flask_login.current_user.get_first_name(),
            logged_in=flask_login.current_user.is_authenticated))

@app.route("/dashboard_admin/<path:username>/discount_codes/create", methods=['GET', 'POST'])
@login_required
def create_discount_code(username):
    creatediscountform = CreateCouponOrPromoPercent(request.form)
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    if request.method == "POST" and creatediscountform.validate():



        coupons_dict = {}

        try:
            db = shelve.open('CustomerCoupons.db', "w")
        except:
            db = shelve.open('CustomerCoupons.db', "c")

        try:
            coupons_dict = db["COUPONS"]
        except:
            print("Unable to retrieve Coupons from coupons.db.")

        name_of_new_discount = creatediscountform.name_of_discount.data
        new_discount_amount = creatediscountform.discount_amount.data
        type_of_new_discount = creatediscountform.type_of_discount.data
        new_discount_code = creatediscountform.discount_code.data
        new_points_required = creatediscountform.points_required.data

        id_of_new_discount = "".join(random.choices(string.ascii_letters + string.digits, k=10))

        if type_of_new_discount == "Promo Code":
            new_discount_blueprint = Promo(id_of_new_discount, name_of_new_discount, new_discount_amount, new_discount_code)
        else:
            new_discount_blueprint = Coupon(id_of_new_discount, name_of_new_discount, new_discount_amount)

        new_discount_blueprint.set_date_of_creation(datetime.now().date())
        new_discount_blueprint.set_status_to_active()
        new_discount_blueprint.set_required_points(new_points_required)



        coupons_dict[id_of_new_discount] = new_discount_blueprint

        db["COUPONS"] = coupons_dict

        db.close()



    return redirect(url_for('admin_view_promo_code', user=str(current_user), username=flask_login.current_user.get_first_name(),
                logged_in=flask_login.current_user.is_authenticated))

    # it will create a stripe coupon which will be embedded into the promo code

@app.route("/dashboard_admin/<path:username>/promo_codes", methods=['GET', 'POST'])
@login_required
def admin_view_promo_code(username):

    creatediscountform = CreateCouponOrPromoPercent(request.form)
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    coupons_dict = {}

    try:
        db = shelve.open('CustomerCoupons.db', "r")
    except:
        db = shelve.open('CustomerCoupons.db', "c")

    try:
        coupons_dict = db["COUPONS"]
    except:
        print("Unable to retrieve Coupons from coupons.db.")

    print(coupons_dict)
    db.close()


    return render_template('manageCoupons.html', user=str(current_user), username=flask_login.current_user.get_first_name(),
                logged_in=flask_login.current_user.is_authenticated, coupons_dict=coupons_dict, form=creatediscountform)

# for user side, they need to have a points account so that they can redeem vouchers


@app.route("/dashboard/<path:username>/redemption_center")
@login_required
def redeem_vouchers(username):
    if not(flask_login.current_user.get_role() == "USER"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    coupons_dict = {}

    try:
        db = shelve.open('CustomerCoupons.db', "r")
    except:
        db = shelve.open('CustomerCoupons.db', "c")

    try:
        coupons_dict = db["COUPONS"]
    except:
        print("Unable to retrieve Coupons from coupons.db.")

    print(coupons_dict)

    # need to get current_user points balance
    points_Accounts = {}
    try:
        db_pointsAccounts = shelve.open('PointsAccounts.db', "r")
    except:
        db_pointsAccounts = shelve.open('PointsAccounts.db', "c")

    try:
        points_Accounts = db_pointsAccounts["Points_Accounts"]
    except:
        print("Unable to retrieve Points Accounts from PointsAccounts.db")
    print(points_Accounts)
    current_user_account = points_Accounts.get(flask_login.current_user.get_id())
    current_points = current_user_account.get_points()

    # need to create user voucher database
    voucher_database = {}


    try:
        db_user_vouchers = shelve.open('UserCoupons.db', "r")
    except:
        db_user_vouchers = shelve.open('UserCoupons.db', "c")

    try:
        voucher_database = db_user_vouchers["USER_VOUCHERS"]
    except:
        print("Unable to retrieve all user vouchers from UserCoupons.db")

    if voucher_database.get(flask_login.current_user.get_id()) == None:
        indi_user_vouchers = {} # dict to store all vouchers related to user
    else:
        indi_user_vouchers = voucher_database.get(flask_login.current_user.get_id())
    print(indi_user_vouchers)
    db_user_vouchers.close()
    db_pointsAccounts.close()
    db.close()

    return render_template('manageUserVouchers.html', points=current_points, user=str(current_user), username=flask_login.current_user.get_first_name(),
                logged_in=flask_login.current_user.is_authenticated, coupons_dict=coupons_dict, voucher_database=indi_user_vouchers)

@app.route("/dashboard/<path:username>/redemption_center/redeem_voucher/<path:coupon_id>/<path:price>/", methods=['GET', 'POST'])
@login_required
def create_voucher(username, coupon_id, price):
    if not(flask_login.current_user.get_role() == "USER"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    coupons_dict = {}

    try:
        db = shelve.open('CustomerCoupons.db', "r")
    except:
        db = shelve.open('CustomerCoupons.db', "c")

    try:
        coupons_dict = db["COUPONS"]
    except:
        print("Unable to retrieve Coupons from coupons.db.")

    print(coupons_dict)

    # need to get current_user points balance
    points_Accounts = {}
    try:
        db_pointsAccounts = shelve.open('PointsAccounts.db', "w")
    except:
        db_pointsAccounts = shelve.open('PointsAccounts.db', "c")

    try:
        points_Accounts = db_pointsAccounts["Points_Accounts"]
    except:
        print("Unable to retrieve Points Accounts from PointsAccounts.db")
    print(points_Accounts)
    current_user_account = points_Accounts.get(flask_login.current_user.get_id())
    current_points = current_user_account.get_points()
    current_user_account.set_points(current_points-int(price))

    db_pointsAccounts["Points_Accounts"] = points_Accounts

    # need to create user voucher database
    voucher_database = {}
    indi_user_vouchers = {} # dict to store all vouchers related to user

    try:
        db_user_vouchers = shelve.open('UserCoupons.db', "w")
    except:
        db_user_vouchers = shelve.open('UserCoupons.db', "c")

    try:
        voucher_database = db_user_vouchers["USER_VOUCHERS"]
    except:
        print("Unable to retrieve all user vouchers from UserCoupons.db")

    voucher_blueprint = coupons_dict.get(coupon_id) # returns a Coupon obj blueprint

    # create stripe coupon from voucher_blueprint
    new_voucher = stripe.Coupon.create(
        percent_off = voucher_blueprint.get_percent()
    )

    # append the Coupon obj to the indi_user_vouchers
    indi_user_vouchers[new_voucher["id"]] = dict(new_voucher)
    voucher_database[flask_login.current_user.get_id()] = indi_user_vouchers
    print(indi_user_vouchers)
    print(voucher_database)
    db_user_vouchers["USER_VOUCHERS"] = voucher_database


    db_user_vouchers.close()
    db_pointsAccounts.close()
    db.close()



    return redirect(url_for("redeem_vouchers", username=flask_login.current_user.get_first_name()))

# used to view current user feedbacks
@app.route("/dashboard/<path:username>/feedback", methods=['GET', 'POST'])
@login_required
def view_user_feedback(username):
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    createfeedbackform = CreateFeedbackForm(request.form)
    feedback_dict = {}
    try:
        db = shelve.open("feedback.db", "r")

    except:
        db = shelve.open("feedback.db", "c")

    try:
        feedback_dict = db["FEEDBACK"]
    except:
        print("Cannot retrieve feedback from feedback.db.")

    print(feedback_dict)

    db.close()

    return render_template("viewUserFeedback.html", username=flask_login.current_user.get_first_name(), user=str(current_user), logged_in=flask_login.current_user.is_authenticated, feedback_dict=feedback_dict, form=createfeedbackform, form_update=createfeedbackform)

# used to view all the user feedbacks
@app.route("/dashboard_admin/<path:username>/feedback", methods=['GET', 'POST'])
@login_required
def view_all_user_feedback(username):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    createfeedbackform = CreateFeedbackForm(request.form)
    feedback_dict = {}
    try:
        db = shelve.open("feedback.db", "r")

    except:
        db = shelve.open("feedback.db", "c")

    try:
        feedback_dict = db["FEEDBACK"]
    except:
        print("Cannot retrieve feedback from feedback.db.")

    db.close()

    return render_template("viewAllUserFeedback.html", username=flask_login.current_user.get_first_name(), user=str(current_user), logged_in=flask_login.current_user.is_authenticated, feedback_dict=feedback_dict, form_update=createfeedbackform)


@app.route("/dashboard/<path:username>/feedback/create", methods=['GET', 'POST'])
@login_required
def create_feedback(username):
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    createfeedbackform = CreateFeedbackForm(request.form)

    if request.method == "POST" and createfeedbackform.validate():
        title = createfeedbackform.title.data
        description = createfeedbackform.description.data
        author = flask_login.current_user.get_first_name()
        date_of_creation = datetime.now().date()
        rating = createfeedbackform.rating.data
        code = "FB_"+str(uuid4())

        # create feedback obj
        new_feedback = Feedback(title, description, author, date_of_creation, rating, code)



        # store new feedback into feedback.db
        feedback_dict = {}
        try:
            db = shelve.open("feedback.db", "w")

        except:
            db = shelve.open("feedback.db", "c")

        try:
            feedback_dict = db["FEEDBACK"]
        except:
            print("Cannot retrieve feedback from feedback.db.")

        feedback_dict[code] = new_feedback


        # update the database
        db["FEEDBACK"] = feedback_dict

        db.close()

        return redirect(url_for("view_user_feedback", username=str(current_user)))


# update the feedback in feedback.db
@app.route("/dashboard/<path:username>/feedback/update/<path:feedback_code>", methods=['GET', 'POST'])
@login_required
def update_feedback(username, feedback_code):
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    createfeedbackform = CreateFeedbackForm(request.form)

    # retrieve feedback from feedback.db
    feedback_dict = {}
    try:
        db = shelve.open("feedback.db", "r")

    except:
        db = shelve.open("feedback.db", "c")

    try:
        feedback_dict = db["FEEDBACK"]
    except:
        print("Cannot retrieve feedback from feedback.db.")

    feedback_to_update = feedback_dict[feedback_code]

    db.close()


    if request.method == "POST" and createfeedbackform.validate():
        title = createfeedbackform.title.data
        description = createfeedbackform.description.data
        date_of_creation = datetime.now().date()
        rating = createfeedbackform.rating.data


        # update feedback obj
        feedback_to_update.set_title(title)
        feedback_to_update.set_description(description)
        feedback_to_update.set_rating(rating)
        feedback_to_update.set_date_of_creation(date_of_creation)


        # store new feedback into feedback.db
        feedback_dict = {}
        try:
            db = shelve.open("feedback.db", "w")

        except:
            db = shelve.open("feedback.db", "c")

        try:
            feedback_dict = db["FEEDBACK"]
        except:
            print("Cannot retrieve feedback from feedback.db.")

        feedback_dict[feedback_code] = feedback_to_update

        # update the database
        db["FEEDBACK"] = feedback_dict

        db.close()

        print("Here")
        return redirect(url_for("view_user_feedback", username=str(current_user)))

    # else:
    #
    #     # autofill form
    #     createfeedbackform.title.data = feedback_to_update.get_title()
    #     createfeedbackform.description.data = feedback_to_update.get_description()
    #     createfeedbackform.rating.data = feedback_to_update.get_rating()

# update the feedback in feedback.db
@app.route("/dashboard_admin/<path:username>/feedback/update/<path:feedback_code>", methods=['GET', 'POST'])
@login_required
def admin_update_feedback(username, feedback_code):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    createfeedbackform = CreateFeedbackForm(request.form)

    # retrieve feedback from feedback.db
    feedback_dict = {}
    try:
        db = shelve.open("feedback.db", "r")

    except:
        db = shelve.open("feedback.db", "c")

    try:
        feedback_dict = db["FEEDBACK"]
    except:
        print("Cannot retrieve feedback from feedback.db.")

    feedback_to_update = feedback_dict[feedback_code]

    db.close()


    if request.method == "POST" and createfeedbackform.validate():
        title = createfeedbackform.title.data
        description = createfeedbackform.description.data
        date_of_creation = datetime.now().date()
        rating = createfeedbackform.rating.data


        # update feedback obj
        feedback_to_update.set_title(title)
        feedback_to_update.set_description(description)
        feedback_to_update.set_rating(rating)
        feedback_to_update.set_date_of_creation(date_of_creation)


        # store new feedback into feedback.db
        feedback_dict = {}
        try:
            db = shelve.open("feedback.db", "w")

        except:
            db = shelve.open("feedback.db", "c")

        try:
            feedback_dict = db["FEEDBACK"]
        except:
            print("Cannot retrieve feedback from feedback.db.")

        feedback_dict[feedback_code] = feedback_to_update

        # update the database
        db["FEEDBACK"] = feedback_dict

        db.close()

        print("Here")
        return redirect(url_for("view_all_user_feedback", username=str(current_user)))



# update the feedback in feedback.db
@app.route("/dashboard/<path:username>/feedback/delete/<path:feedback_code>", methods=['GET', 'POST'])
@login_required
def delete_feedback(username, feedback_code):
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    if request.method == "POST":

        # retrieve all the feedback
        feedback_dict = {}
        try:
            db = shelve.open("feedback.db", "w")

        except:
            db = shelve.open("feedback.db", "c")

        try:
            feedback_dict = db["FEEDBACK"]
        except:
            print("Cannot retrieve feedback from feedback.db.")

        # delete the feedback from the feedback_dict
        feedback_dict.pop(feedback_code)

        # update feedback.db
        db["FEEDBACK"] = feedback_dict

        db.close()


        return redirect(url_for("view_user_feedback", username=str(current_user)))

# update the feedback in feedback.db
@app.route("/dashboard_admin/<path:username>/feedback/delete/<path:feedback_code>", methods=['GET', 'POST'])
@login_required
def admin_delete_feedback(username, feedback_code):
    if not(flask_login.current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    current_user = username

    if request.method == "POST":

        # retrieve all the feedback
        feedback_dict = {}
        try:
            db = shelve.open("feedback.db", "w")

        except:
            db = shelve.open("feedback.db", "c")

        try:
            feedback_dict = db["FEEDBACK"]
        except:
            print("Cannot retrieve feedback from feedback.db.")

        # delete the feedback from the feedback_dict
        feedback_dict.pop(feedback_code)

        # update feedback.db
        db["FEEDBACK"] = feedback_dict

        db.close()


        return redirect(url_for("view_all_user_feedback", username=str(current_user)))

# view AR Model
@app.route("/AR_PC1")
@login_required
def view_model():
    if not(flask_login.current_user.get_role() == "USER" or flask_login.current_user.get_role() == "GUEST"):
        if flask_login.current_user.get_role() == "ADMIN":
            return redirect(url_for('get_admin_dashboard', username=flask_login.current_user.get_first_name()))
        return redirect(url_for('get_dashboard', username=flask_login.current_user.get_first_name()))

    return render_template("dashboard_AR_pc.html", user=current_user.get_first_name(), logged_in=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True)
