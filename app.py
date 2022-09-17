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

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post_submit(user_id):
    title = request.form["title"]
    content = request.form["content"]
    user = user_id
    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Shows a single post"""
    post = Post.query.get(post_id)
    user = User.query.get(post.user)
    return render_template("post_details.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post(post_id):
    """Edit a post"""
    post = Post.query.get(post_id)
    user = User.query.get(post.user)
    return render_template("edit_post.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_submuit(post_id):
    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post"""
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect("/users")