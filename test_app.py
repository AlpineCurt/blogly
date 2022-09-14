from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for viewing, editing, and deleting Users"""

    def setUp(self):
        """Add test users"""

        User.query.delete()

        user1 = User(first_name = "Alex",
        last_name = "Mack",
        image_url = "secretworld.com")

        db.session.add(user1)
        db.session.commit()

        self.user_id = user1.id
    
    def tearDown(self):
        
        db.session.rollback()
    
    def test_user_list(self):
        """Page displaying all users in database"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Alex", html)
        
    def test_user_id(self):
        """Display info about single user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Alex", html)
            self.assertIn("Edit", html)
    
    def test_create_user(self):
        """Page for creating a new user"""
        with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/users/new" method="POST">', html)
    
    def test_edit_user_post(self):
        """Submitting a POST request editing a user"""
        with app.test_client() as client:
            update_info = {'first_name' : "Dustin",
            'last_name' : "Henderson",
            'image_url' : "strangerthings.com"}

            resp = client.post(f"/users/{self.user_id}/edit", data=update_info)
            html = resp.get_data(as_text=True)

            test_user = User.query.get(self.user_id)

            self.assertEqual(test_user.first_name, "Dustin")
            self.assertEqual(test_user.last_name, "Henderson")
            self.assertEqual(test_user.image_url, "strangerthings.com")