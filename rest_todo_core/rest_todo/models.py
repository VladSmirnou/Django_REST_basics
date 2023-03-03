from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class UserPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_body = models.CharField(max_length=100)

    class Meta:
        # Django shows a warning without this ordering
        ordering = ['id']