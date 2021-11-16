from django.http import response
from django.test import TestCase
from django.test.client import Client
from network.models import *
from django.urls import reverse


class IndexViewTest(TestCase):

    # Setup test data
    @classmethod
    def setUpTestData(cls):
        # Create 5 users and 5 posts
        username = ['a', 'b', 'c', 'd', 'f']
        for i in username:
            i = User.objects.create(username=i, password="123")
            Post.objects.create(poster=i, content="testcontent")

    def test_redirect_if_not_signed_in(self):
        c = Client()
        response = c.get("")
        self.assertRedirects(response, '/login/')

    def test_signedin_use_correct_template(self):
        c = Client()
        user_a = User.objects.get(id=1)
        # Force login
        c.force_login(user_a)
        response = c.get("")

        # Check if the user is logged in
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'a')

        # Check if the template is correct
        self.assertTemplateUsed(response, 'network/index.html')

# TODO this test run into erros

    def test_navbar_urls_corret(self):
        c = Client()
        user_a = User.objects.get(id=1)
        c.force_login(user_a)
        response = c.get(reverse('mypage'))
        self.assertEqual(response.status_code, 200)
