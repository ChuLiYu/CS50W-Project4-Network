from django.test import TestCase, Client
from .models import User, Post, Following, Like

# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):

        # create users
        u1 = User.objects.create(username="AAA", password="AAA")
        u2 = User.objects.create(username="BBB", password="BBB")
        u3 = User.objects.create(username="ccc", password="ccc")

        # create posts
        Post.objects.create(creator=u1, context="Context1")

        Post.objects.create(creator=u2, context="Context1")
        Post.objects.create(creator=u1, context="Context2")
        Post.objects.create(creator=u1, context="Context3")
        Post.objects.create(creator=u1, context="Context4")

    def test_user_post_count(self):
        u = User.objects.get(username="AAA")
        p = Post.objects.filter(creator=u)
        self.assertEqual(p.count(), 4)

    # Client Testing
    def test_index(self):
        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

    def test_following(self):
        c = Client()
        response = c.get("/following/")
        self.assertEqual(response.status_code, 404)
