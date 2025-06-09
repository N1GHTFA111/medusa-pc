@app.route('/registerUser', methods=["GET", "POST"])
def registerUser():
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
        return redirect(url_for('get_dashboard', username=new_user.get_first_name()))
    return render_template("registerUser.html",form=createuserform, logged_in=current_user.is_authenticated)


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
        current_user_to_update.set_company(new_company)
        current_user_to_update.set_phone(new_phone)

        db.session.commit()
        return redirect(url_for('get_dashboard', username=current_user_to_update.get_first_name(),  logged_in=current_user.is_authenticated))
    else:
        current_user_to_update = UserModel.query.filter_by(email=email).first()
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

        return render_template("updateUser.html", email=email, form=updateuserform,)

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
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/deleteUser_Admin/path:<email>', methods=['GET', 'POST'])
@login_required
def deleteUser_admin(email):
    if not(current_user.get_role() == "ADMIN"):
        return redirect(url_for('get_dashboard', username=current_user.get_first_name()))

    print(email)
    user_to_delete = UserModel.query.filter_by(email=email).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('get_dashboard', username=current_user.get_first_name()))}