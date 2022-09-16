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

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    user_id = db.relationship('User', backref="posts")

    @classmethod
    def get_posts_by_user_id(cls, user_id):
        return cls.query.filter_by(user=user_id).all()