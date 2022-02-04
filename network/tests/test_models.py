from django.test import TestCase
from network.models import *


class UserFollowingTest(TestCase):
    # Setup test data
    @classmethod
    def setUpTestData(cls):

        user1 = User.objects.create(username="a")
        user2 = User.objects.create(username="b")
        user3 = User.objects.create(username="c")

        # Create userfollowing objects
        userfollowing1 = UserFollowing.objects.create(
            user=user1, following_user=user2)
        userfollowing2 = UserFollowing.objects.create(
            user=user1, following_user=user3)

        # Create post objects
        Post.objects.create(poster=user1, content="test1")
        Post.objects.create(poster=user1, content="test2")

    def test_user_follows(self):
        user1 = User.objects.get(username='a')
        user1_follows = user1.follows()
        self.assertEqual(len(user1_follows), 2)
        self.assertEqual(user1_follows[0], "b")
        self.assertEqual(user1_follows[1], "c")

    def test_user_followed_by(self):
        user2 = User.objects.get(username='b')
        user2_followed_by = user2.followed_by()
        self.assertEqual(len(user2_followed_by), 1)
        self.assertEqual(user2_followed_by[0], "a")

    def test_user_as_foreignkey_of_posts(self):
        user1 = User.objects.get(username='a')
        user1_posts = user1.posts.all()
        self.assertEqual(len(user1_posts), 2)
        self.assertEqual(user1.posts_content()[0], "test1")

    def test_serialize_returns_dictionary(self):
        user1 = User.objects.create(username="d")
        Post.objects.create(poster=user1, content="test1")
        post1 = Post.objects.get(poster=user1)
        self.assertTrue((type(post1.serialize()) is dict), True)
        self.assertEqual(post1.serialize()['poster'], "d")
        self.assertEqual(post1.serialize()['content'], "test1")
