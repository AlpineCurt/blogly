"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
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

@app.route("/users/new", methods=["GET"])
def new_user():
    """Shows form to create a new user"""
    return render_template('new_user.html')

@app.route("/users/new", methods=["POST"])
def create_user():
    """Adds user to database"""
    return "<h1>YOU POSTED!  YAAAAAY!</h1>"