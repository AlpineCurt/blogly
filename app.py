"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "vSCHQCdctw"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
#db.create_all()

@app.route("/")
def home_page():
    return redirect("/users")

@app.route("/users")
def user_list():
    """Shows list of all users"""
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a user"""
    user = User.query.get_or_404(user_id)
    posts = Post.get_posts_by_user_id(user_id)
    return render_template("user_details.html", user=user, posts=posts)

@app.route("/users/new", methods=["GET"])
def new_user():
    """Shows form to create a new user"""
    return render_template('new_user.html')

@app.route("/users/new", methods=["POST"])
def create_user():
    """Adds user to database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    """Edit a user's info"""
    user = User.query.get_or_404(user_id)
    
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_post(user_id):
    """Submit edits to a user's info"""
    update_info = dict(request.form)
    user = User.get_user_by_id(user_id)
    user.update_user(update_info)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post(user_id):
    """Display page for createing a new post"""
    user = User.get_user_by_id(user_id)
    return render_template("new_post.html", user=user)
