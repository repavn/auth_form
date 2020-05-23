from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_news = models.BooleanField(verbose_name='Receive news and etc.', default=True, blank=True)

    def __str__(self):
        return 'Extra info about user'
