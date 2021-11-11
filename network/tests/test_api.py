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
        api_testuser = User.objects.get(id=1)
        c.force_login(api_testuser)
        # If request through GET, it returns false
        response = c.get('/makepost/')
        self.assertEqual(json.loads(response.content)['ok'], False)
        # TODO is this the right way to pass a request data to the api?
        response = c.post(
            '/makepost/', content_type="application/json", data={"content": "testing api content"})
        self.assertEqual(json.loads(response.content)['ok'], True)
        # Check if a new post object is created
        self.assertTrue(Post.objects.filter(
            content="testing api content").exists())

    def test_getposts_api(self):
        c = Client()
        api_testuser = User.objects.get(id=1)
        c.force_login(api_testuser)
        # If its the wrong group, returns an error message
        response = c.get("/getposts/wronggroup/",
                         HTTP_ACCEPT='application/json')
        self.assertEqual(json.loads(response.content)
                         ["error"], "Invalid group.")

        # If it request for all_users, return all the posts
        response = c.get("/getposts/all_users/",
                         HTTP_ACCEPT='application/json')
        all_posts = json.loads(response.content)
        self.assertEqual(len(all_posts), 3)

        # If it requests for this_user, only return posts of user1

        response = c.get("/getposts/this_user/",
                         HTTP_ACCEPT='application/json')
        user1_post = json.loads(response.content)
        self.assertEqual(len(user1_post), 1)

        # If it requests for following users, return posts of user2

        response = c.get("/getposts/followed_user/",
                         HTTP_ACCEPT='application/json')
        followed_user_post = json.loads(response.content)
        self.assertEqual(len(followed_user_post), 2)


class TestIsFollowingAPI(TestCase):

    def test_is_following_or_not(self):
        # Test the is_following API route
        # Setup test data
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
        u3 = User.objects.create(username="c")
        UserFollowing.objects.create(user=u1, following_user=u2)

        # Use test client and force logi
        c = Client()
        c.force_login(u1)

        # u1 follows u2 api returns true
        response = c.get("/mypage/2/is_following/",
                         HTTP_ACCEPT="application/json")
        self.assertEqual(json.loads(response.content)["isFollowing"], True)

        # u1 is following u3 api returns false
        response = c.get("/mypage/3/is_following/",
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
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
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
        u1 = User.objects.create(username="a")
        u2 = User.objects.create(username="b")
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
