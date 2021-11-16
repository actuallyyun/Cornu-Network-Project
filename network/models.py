from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class User(AbstractUser):
    pass

    def follows(self):
        return [u.following_user.username for u in self.following.all()]

    def followed_by(self):
        return [f.user.username for f in self.followers.all()]

    def follows_user_object(self):
        return [u.following_user for u in self.following.all()]

    def posts_content(self):
        return [p.content for p in self.posts.all()]

    def num_follows(self):
        return self.following.all().count()

    def num_followers(self):
        return self.followers.all().count()

    def posts_followed_user(self):

        posts = []
        for u in self.follows_user_object():
            post_queryset = Post.objects.filter(poster=u).order_by(
                "-date_time_created")
            for p in post_queryset:
                posts.append(p)

        return posts


class UserFollowing(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")

    # TODO A user shouldn't be able to follow herself, add a constraint to the database following_user != user

    class Meta:
        unique_together = ['user', 'following_user']

    def __str__(self):
        return f'{self.user}'


class Post(models.Model):
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")

    content = models.TextField()
    date_time_created = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            "poster": self.poster.username,
            "content": self.content,
            "timestamp": self.date_time_created.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

    def time_posted(self):
        return self.date_time_created.strftime("%b %d")

    def poster_id(self):
        return User.objects.get(username=self.poster).id

    def likes(self):
        return self.liked.all().count()


class PostLiking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liking")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="liked")

    class Meta:
        unique_together = ['user', 'post']
