from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    info = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together =('email',)

    def __str__(self):
        return self.username


class Tweet(models.Model):
    content = models.TextField(max_length=300)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disabled = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('tweet_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.content


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='receiver')
    content = models.TextField(max_length=300)
    read = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def is_read_message(self):
        if self.read:
            return 'read'
        else:
            return 'unread'

    def change_to_read(self):
        if not self.read:
            self.read = True
            self.save()
        return ''


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.content

