from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email_address' # plesse use your email address 
app.config['MAIL_PASSWORD'] = 'generate_your app_password of your email'   # please generate your app password'

mail = Mail(app)


with app.app_context():
    # Create all tables defined in the SQLAlchemy models
    db.create_all()  
    # Remember this db.create_all() is not working properply..... you have to create the tables manually.... 

from Kaman_Blog import routes

