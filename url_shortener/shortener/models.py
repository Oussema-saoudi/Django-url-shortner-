from django.db import models
from django.contrib.auth.models import User


class Urls(models.Model):
    short_form = models.CharField(max_length=255)
    original_form = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nbr_visit = models.IntegerField(default=0)
