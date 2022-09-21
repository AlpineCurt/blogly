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

    posts = db.relationship('Post', cascade="all, delete-orphan", backref="user")

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    tags = db.relationship('Tag', secondary='post_tags', passive_deletes=True, cascade="all, delete")
    
    @classmethod
    def get_posts_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)

    posts = db.relationship('Post', secondary='post_tags', passive_deletes=True, cascade="all, delete")


class PostTag(db.Model):

    __tablename__ = "post_tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    tag = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True, nullable=False)