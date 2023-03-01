from app import db
from flask_authorize import RestrictionsMixin


# note_category = db.Table('note_category', db.metadata,
#     db.Column('id', db.Integer , primary_key=True),
#     db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
#     db.Column('note_id', db.Integer, db.ForeignKey('notes.id'))
# )


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    notes = db.relationship("Note", backref="categories", cascade='all, delete')

 
    def __init__(self, category_name):
        # self.id = id
        self.category_name = category_name