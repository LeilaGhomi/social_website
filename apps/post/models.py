from math import floor

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import now

from apps.account.models import User
from apps.post.managers import PostManager


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    created_date = models.DateTimeField(default=now)
    account_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = PostManager()

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    @property
    def age(self):
        """
        get created date that Automatic save
        :return: How long the post has been published.
        """
        age = timezone.now() - self.created_date
        age_year = age.days / 365
        age_month = age.days / 30
        age_day = age.days
        age_hour = (age.seconds / 60) / 60
        if age_year >= 1:
            return '{} years a go'.format(floor(age_year))
        elif age_month >= 1:
            return '{} months a go'.format(floor(age_month))
        elif age_day >= 1:
            return '{} days a go'.format(floor(age_day))
        elif age_hour >= 1:
            return '{} hours a go'.format(floor(age_hour))
        else:
            return 'recently'


class Comment(models.Model):
    note = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=now)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.note


class Like(models.Model):
    created_date = models.DateTimeField(default=now)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']
        unique_together = ('post_id', 'user_id',)

    def __str__(self):
        return str(self.user_id)
