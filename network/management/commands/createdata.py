from lib2to3.pytree import Base
from pdb import post_mortem
from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from network.models import User, UserFollowing, Post, PostLiking
import random


class Provider(faker.providers.BaseProvider):

    def network_user(self):
        return self.random_element(list(User.objects.all()))

    def network_post(self):
        return self.random_element(list(Post.objects.all()))


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(Provider)

        # Generate users
        for _ in range(20):
            # User.objects.create(username=fake.unique.first_name(), email=fake.unique.ascii_email(),
            #                     password=fake.bothify(text='###????##?????#####'))
            Post.objects.create(poster=fake.network_user(), content=fake.paragraph(
                nb_sentences=8, variable_nb_sentences=True))
            # UserFollowing.objects.create(
            #     user=fake.network_user(), following_user=fake.network_user())
            # PostLiking.objects.create(
            #     user=fake.network_user(), post=fake.network_post())
