from django.http import response
from django.test import TestCase
from django.test.client import Client
from network.models import *
import json

from network.views import following


class TestMakePostAPI(TestCase):
    # Setup test data
    @classmethod
    def setUpTestData(cls):
        # Create 3 users
        u1 = User.objects.create(username="api_testuser1", password="password")
        u2 = User.objects.create(username="api_testuser2", password="password")
        u3 = User.objects.create(username="api_testuser3", password="password")

        # Create some following relationships
        f1 = UserFollowing.objects.create(user=u1, following_user=u2)
        f1 = UserFollowing.objects.create(user=u1, following_user=u3)

        # Create some posts
        Post.objects.create(poster=u1, content="posts of user1")
        Post.objects.create(poster=u2, content="post of user2")
        Post.objects.create(poster=u2, content="user2 has another post")

    def test_makepost_api(self):
        c = Client()
        api_testuser = User.objects.get(username="api_testuser1")
        c.force_login(api_testuser)
        # If request through GET, it returns false
        response = c.get('/makepost/')
        self.assertEqual(json.loads(response.content)['ok'], False)
        response = c.post(
            '/makepost/', content_type="application/json", data={"content": "testing api content"})
        self.assertEqual(json.loads(response.content)['ok'], True)
        # Check if a new post object is created
        self.assertTrue(Post.objects.filter(
            content="testing api content").exists())


class TestIsFollowingAPI(TestCase):

    def test_is_following_or_not(self):
        # Test the is_following API route
        # Setup test data
        u1 = User.objects.create(username="a", pk=1)
        u2 = User.objects.create(username="b", pk=2)
        u3 = User.objects.create(username="c")
        UserFollowing.objects.create(user=u1, following_user=u2)

        # Use test client and force logi
        c = Client()
        c.force_login(u1)

        # u1 follows u2 api returns true
        response = c.get("/users/2/is_following/",
                         HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)["isFollowing"], True)

        # u1 is following u3 api returns false
        response = c.get("/users/3/is_following/",
                         HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)["isFollowing"], False)


class TestFollowUserAPI(TestCase):

    def test_request_method_is_put(self):
        c = Client()
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        c.force_login(u1)
        response = c.get("/mypage/2/follow_user/follow",
                         HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)[
                         'error'], 'PUT request required')

    def test_follow_user_correcty(self):
        # Create test data
        c = Client()
        u1 = User.objects.create(username="a", pk=1)
        u2 = User.objects.create(username="b", pk=2)
        c.force_login(u1)

        response = c.put("/mypage/2/follow_user/follow",
                         HTTP_ACCEPT="application/json")

        # Assert the correct Jason respons and the data is created
        self.assertEqual(json.loads(response.content)[
                         'message'], 'Followed successfully')
        self.assertTrue(UserFollowing.objects.filter(
            user=u1, following_user=u2).exists())

    def test_unfollow_user_correcty(self):
        # Create test data
        c = Client()
        u1 = User.objects.create(username="a", pk=1)
        u2 = User.objects.create(username="b", pk=2)
        UserFollowing.objects.create(user=u1, following_user=u2)
        c.force_login(u1)

        response = c.put("/mypage/2/follow_user/unfollow",
                         HTTP_ACCEPT="application/json")

        # Assert the correct Jason respons and the data is created
        self.assertEqual(json.loads(response.content)[
                         'message'], 'Unfollowed successfully')
        self.assertFalse(UserFollowing.objects.filter(
            user=u1, following_user=u2).exists())


class TestEditPostAPI(TestCase):

    def test_request_method_is_put(self):
        # Create test data
        c = Client()
        u1 = User.objects.create(username="a")
        c.force_login(u1)

        response = c.get("/editpost/", HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)[
                         'error'], 'PUT request required')

    def test_update_post_correctly(self):
        # Create test data

        c = Client()
        u1 = User.objects.create(username="a")
        c.force_login(u1)

        p1 = Post.objects.create(poster=u1, content="original texts")
        response = c.put("/editpost/", content_type="application/json",
                         data={"content": "updated texts", "post_id": "1"})
        self.assertEqual(json.loads(response.content)['ok'], True)
        self.assertEqual(Post.objects.get(pk=1).content, "updated texts")


class TestIsLikingAPI(TestCase):

    def test_is_liking_or_not_correctly(self):
        # Test the is_following API route
        # Setup test data
        u1 = User.objects.create(username="a", pk=1)
        u2 = User.objects.create(username="b", pk=2)
        p1 = Post.objects.create(poster=u2, pk=1)
        p2 = Post.objects.create(poster=u2, pk=2)
        PostLiking.objects.create(user=u1, post=p1)

        # Use test client and force logi
        c = Client()
        c.force_login(u1)

        # u1 isliking post1 api returns true
        response = c.get("/following/is_liking/1",
                         HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)["isLiking"], True)

        # u1 is not liking post2 api returns false
        response = c.get("/following/is_liking/2",
                         HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)["isLiking"], False)


class TestLikeUnlikeAPI(TestCase):

    def test_request_method_is_put(self):
        # Create test data
        c = Client()
        u1 = User.objects.create(username="a")
        c.force_login(u1)

        response = c.get("/following/like_unlike/like",
                         HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)[
                         'error'], 'PUT request required')

    def test_like_unlike_correctly(self):

        # Setup test data
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        p1 = Post.objects.create(poster=u2, pk=1)
        p2 = Post.objects.create(poster=u2, pk=2)
        PostLiking.objects.create(user=u1, post=p2)

        c = Client()
        c.force_login(u1)

        # u1 likes p1
        response = c.put('/following/like_unlike/like', content_type="application/json",
                         data={"post_id": "1"})
        # Check if returns the correct response
        self.assertEqual(json.loads(response.content)[
                         'message'], "Liked successfully")
        # Check if database is updated accordingly
        self.assertTrue(PostLiking.objects.filter(user=u1, post=p1).exists())

        # u2 unlikes p2
        response = c.put('/following/like_unlike/unlike', content_type="application/json",
                         data={"post_id": "2"})
        # Check if returns the correct response
        self.assertEqual(json.loads(response.content)[
                         'message'], "Unliked successfully")
        # Check if database is updated accordingly
        self.assertFalse(PostLiking.objects.filter(user=u1, post=p2).exists())
