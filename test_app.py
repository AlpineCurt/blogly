from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for viewing, editing, and deleting Users"""

    def setUp(self):
        """Clear the database"""
        db.drop_all()
        db.create_all()

        """Add a test user"""
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

class PostsTestCase(TestCase):

    def setUp(self):
        """Reset the test database"""
        db.drop_all()
        db.create_all()
        
        """Add some test users"""
        self.u1 = User(first_name="Jeff", last_name="Goldblum", image_url=f"https://d26oc3sg82pgk3.cloudfront.net/files/media/edit/image/21525/square_thumb%402x.jpg")
        self.u2 = User(first_name="Stevie", last_name="Budd", image_url="https://img.sharetv.com/shows/characters/thumbnails/schitts_creek_ca.stevie_budd.jpg")

        db.session.add_all([self.u1, self.u2])
        db.session.commit()

        """Add some test posts"""
        self.p1 = Post(title="In the Jeep", content="Getting chased by a T-Rex and this guy won't drive any faster.  fml", user=1)
        self.p2 = Post(title="Ew, David!", content="I'm not the one that says Ew, David", user=2)

        db.session.add_all([self.p1, self.p2])
        db.session.commit()

    def tearDown(self):
        """Clear any botched commits"""
        db.session.rollback()
    
    def test_user_details(self):
        """Testing display of user's posts"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.u1.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jeep", html)
    
    def test_new_post_page(self):
        """display of new post page/form"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.u1.id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="title">Title</label>', html)
    
    def test_new_post_submit(self):
        """Submitting a POST request creating a blog post"""
        with app.test_client() as client:
            test_data = {'title' : "Must Go Faster",
            'content' : "T Rex is chasing us"}
            resp = client.post(f"/users/{self.u1.id}/posts/new", data=test_data)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

            test_post = Post.query.get(3)

            self.assertEqual(test_post.title, "Must Go Faster")
            self.assertEqual(test_post.content, "T Rex is chasing us")
    
    def test_edit_post_submit(self):
        """Submitting POST request editing an existing blog post"""
        with app.test_client() as client:
            test_data = {'title' : "Are we Human",
            'content' : "Or are we dancers"}
            resp = client.post(f"/posts/{self.p2.id}/edit", data=test_data)

            self.assertEqual(resp.status_code, 302)

            test_post = Post.query.get(2)

            self.assertEqual(test_post.title, "Are we Human")
            self.assertEqual(test_post.content, "Or are we dancers")