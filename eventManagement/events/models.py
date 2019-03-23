from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class event(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    venue = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    registered_users = models.ManyToManyField(User, related_name='registered_user',null=True,blank=True)
    private = models.BooleanField(default=False)
    invited_users = models.ManyToManyField(User, related_name='invited_users',null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
