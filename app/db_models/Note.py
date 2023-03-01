from app import db
from flask_authorize import PermissionsMixin
from app.db_models.User import User

class Note(db.Model):
    __tablename__= "notes"
    # __permissions__= dict(
    #     category = ['read','update']
    # )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    text = db.Column(db.String())
    picture = db.Column(db.String(), nullable=True, default='default.png') 

    id_category = db.Column(db.Integer, db.ForeignKey('categories.id') )
    # categories = db.relationship("Category", secondary="note_category", backref=db.backref("users", lazy="dynamic"))

    def __init__(self, name ,text, id_category, picture):
        self.name = name
        self.text = text
        self.picture = picture
        self.id_category = id_category