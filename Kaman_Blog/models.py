from Kaman_Blog import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, default="default.jpg", nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def get_token(self, expires_sec=1800):
        serial = Serializer(app.config['SECRET_KEY'],expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)
        except:
            return None
        return User.query.get(user_id['user_id'])

    def __repr__(self):
       return f"User('{self.username}', '{self.email}', '{self.date_created}')"
   
   
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(20), unique=False, nullable=False)
    message = db.Column(db.String(80), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Contact('{self.name}', '{self.email}', '{self.subject}', '{self.message}', '{self.date_created}')"