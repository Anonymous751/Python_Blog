from flask import render_template, redirect, url_for, request, flash, session
from Kaman_Blog import app, db, bcrypt, mail
from Kaman_Blog.forms import RegisterForm, LoginForm, ContactForm, ResetRequestForm, ResetPasswordForm, AccountUpdateForm
from Kaman_Blog.models import User, Contact
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import json
import os


with open('Kaman_Blog/config.json') as c:
    params = json.load(c)["params"]

@app.route("/", methods=['GET', 'POST'])
def homepage():
    form = ContactForm()
    if form.validate_on_submit():
        user12 = Contact(name=form.name.data, email=form.email.data, subject=form.subject.data, message=form.message.data)
        print(user12)
        db.session.add(user12)
        db.session.commit()
        return redirect(url_for('contact'))
    show_list_items = True 
    return render_template("index.html", show_list_items=show_list_items, params=params, form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'You are logged in as {form.email.data}!', category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Login unsuccessful. Please check email and password', category='danger')
            return redirect(url_for('login'))
    show_list_items = False 
    hide_list_items = True 
    return render_template("login.html", show_list_items=show_list_items, hide_list_items=hide_list_items, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegisterForm()
    if form.validate_on_submit():
        encrypted_password =  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('login'))
    show_list_items = False
    hide_list_items = True 
    return render_template("register.html", show_list_items=show_list_items, hide_list_items=hide_list_items, form=form)


def save_picture(form_picture):
    picture_name = form_picture.filename
    picture = os.path.join(app.root_path, 'static/profile_pic', picture_name)
    form_picture.save(picture)
    return picture_name


@app.route("/account", methods=['GET', 'POST'])
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        
        
         # this image_file field is created in model to be used ... first you created it .. Please check the model for more info . 
        
        image_file = save_picture(form.picture.data)
        
        current_user.image_file = image_file 
        
        # Make sure the image_file field is present in the database 
       
        db.session.commit()
        return redirect(url_for('account'))
    image_url = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template("account.html", form=form, legend ='Account Page', params=params, image_url=image_url)
    
@app.route("/logout")
def logout():
    show_list_items = False
    logout_user()
    return render_template("logout.html",  show_list_items = show_list_items)

@app.route("/contact")
def contact():
    return render_template("contact.html")

def sent_mail(user):
    token = user.get_token()
    reset_url = url_for('reset_token', token=token, _external=True)
    msg = Message('Password Reset Request', sender='Kaman', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    
    {reset_url}
     .....
     
     if you did not make this request then simply ignore this email and no changes will be made.
     .....
     
     
     '''
    print(f"Reset URL: {reset_url}")
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            sent_mail(user)
            flash("Reset Request Sent ! Please check your email ", "success")
            return redirect(url_for('login'))
    return render_template("reset_request.html", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password =  hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("change_password.html", form=form)