from app import db
from flask_login import UserMixin
# from app.db_models.Group import user_group

class User(db.Model, UserMixin):
    __tablename__ = "all_users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    

    def __init__(self, name, email , password):
        self.name = name
        self.email = email
        self.password = password