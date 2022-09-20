from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

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
        self.p1 = Post(title="In the Jeep", content="Getting chased by a T-Rex and this guy won't drive any faster.  fml", user_id=1)
        self.p2 = Post(title="Ew, David!", content="I'm not the one that says Ew, David", user_id=2)

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
    
    def test_delete_post(self):
        """Test deleting a post.  Users should be untouched"""
        with app.test_client() as client:
            post1 = Post.query.filter_by(id=2).first()
            self.assertNotEqual(post1, None) # Verify post exists before testing deletion

            resp = client.post("/posts/2/delete")
            post2 = Post.query.filter_by(id=2).first()
            users = User.query.all()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(post2, None)  # The same same post should now be gone
            self.assertEqual(len(users), 2) # Users should be untouched
    
    def test_delete_user(self):
        """Test deleting user.  User's posts should be deleted.
        Other users and posts should be untouched."""
        with app.test_client() as client:
            '''Verify post and user exist before deleting'''
            post1 = Post.query.filter_by(id=1).first()
            user1 = User.query.filter_by(id=1).first()
            user4 = User.query.filter_by(id=4).first()
            self.assertNotEqual(post1, None)
            self.assertNotEqual(user1, None)
            self.assertEqual(user4, None)

            resp = client.post("/users/1/delete")

            '''user1 and post1 should be gone, and others should remain'''
            post1 = Post.query.filter_by(id=1).first()
            user1 = User.query.filter_by(id=1).first()
            post2 = Post.query.filter_by(id=2).first()
            user2 = User.query.filter_by(id=2).first()
            self.assertEqual(user1, None)
            self.assertEqual(post1, None)
            self.assertNotEqual(post2, None)
            self.assertNotEqual(user2, None)

class TagsTestCase(TestCase):

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
        self.p1 = Post(title="In the Jeep", content="Getting chased by a T-Rex and this guy won't drive any faster.  fml", user_id=1)
        self.p2 = Post(title="Ew, David!", content="I'm not the one that says Ew, David", user_id=2)

        db.session.add_all([self.p1, self.p2])
        db.session.commit()

        """Add some test tags"""
        self.t1 = Tag(name="cute")
        self.t2 = Tag(name="funny")
        self.t3 = Tag(name="political")

        db.session.add_all([self.t1, self.t2, self.t3])
        db.session.commit()

        """Add the tags to the posts via post_tags table"""
        self.pt1 = PostTag(post=1, tag=2)
        self.pt2 = PostTag(post=2, tag=2)
        self.pt3 = PostTag(post=1, tag=3)

        db.session.add_all([self.pt1, self.pt2, self.pt3])
        db.session.commit()

    def tearDown(self):
        """Clear any botched commits"""
        db.session.rollback()

    def test_delete_tag(self):
        """Delete a tag.  Post and user should remain.
        Related PostTags should be deleted"""
        with app.test_client() as client:
            """Verify post, user, tag, and posttags exist before altering"""
            post = Post.query.get(1)
            user = User.query.get(1)
            tag = Tag.query.get(2)
            posttags = PostTag.query.filter(PostTag.post==1).all()

            self.assertEqual(post.title, "In the Jeep")
            self.assertEqual(user.first_name, "Jeff")
            self.assertEqual(tag.name, "funny")
            self.assertEqual(len(posttags), 2)

            resp = client.post("/tags/2/delete")
            tag1 = Tag.query.filter_by(id=2).first()
            post1 = Post.query.filter_by(id=1).first()
            post2 = Post.query.filter_by(id=2).first()
            user1 = User.query.filter_by(id=1).first()
            posttag1 = PostTag.query.filter(PostTag.post==1).all()
            posttag2 = PostTag.query.filter(PostTag.post==2).all()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(tag1, None)  # Tag should be gone
            self.assertNotEqual(post1, None)  # First Post that had the tag should remain
            self.assertNotEqual(post2, None)  # Second Post that had the tag should remain
            self.assertNotEqual(user1, None)  # User should remain
            self.assertEqual(len(posttag1), 1) # Post 1 should have one tag now
            self.assertEqual(len(posttag2), 0) # Post 2 should have no tags now

    def test_delete_post(self):
        """Delete a Post.  Tags should remain.
        Related rows in post_tags should be deleted."""
        with app.test_client() as client:
            resp = client.post("/posts/1/delete")
            tags = Tag.query.all()
            posttags = PostTag.query.all()

            self.assertEqual(len(tags), 3)  # Tags should remain
            self.assertEqual(len(posttags), 1)  # two post_tag rows should be gone.