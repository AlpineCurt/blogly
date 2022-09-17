from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for User Model"""

    def setUp(self):
        """Make sure user table is clear"""

        User.query.delete()
    
    def tearDown(self):
        
        db.session.rollback()

    def test_update_user(self):

        update_data = {'first_name' : "Harry",
        "last_name" : "Winston",
        "image_url" : "http://www.harrywinston.com"}

        test_user = User(first_name = "Bella", last_name = "Donna", image_url = "cheapassjewelry.com")
        test_user.update_user(update_data)

        self.assertEqual(test_user.first_name, "Harry")
        self.assertEqual(test_user.last_name, "Winston")
        self.assertEqual(test_user.image_url, "http://www.harrywinston.com")

class PostModelTestCase(TestCase):
    """Tests for Post Model"""

    def setUp(self):
        Post.query.delete()
    
    def tearDown(self):
        db.session.rollback()