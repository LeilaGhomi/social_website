from django.db import models


class PostManager(models.Manager):
    def user_post(self, user):
        posts = self.filter(user=user)
        return posts
