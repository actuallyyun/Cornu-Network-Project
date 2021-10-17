from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class User(AbstractUser):
    pass

    def follows(self):
        return [u.following_user_id.username for u in self.following.all()]

    def followed_by(self):
        return [f.user_id.username for f in self.followers.all()]


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")

# A user should have a followers filed and a follows field.
# These fields should be linked to User model using ForeignKeys


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
# TODO Other arguments to add to the poster field

    content = models.TextField()
    date_time_created = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
