"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.get(user_id)
    
    def update_user(self, update_info):
        """Updates all fields from dictionary user_info"""
        for key in update_info:
            setattr(self, key, update_info[key])