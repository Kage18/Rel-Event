from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Group(models.Model):  

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='members')


class Group_invite(models.Model):

    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    to = models.ForeignKey(User, related_name="invitedtogroup",null=True,  blank=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class Group_request(models.Model):
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    request_from = models.ForeignKey(User, related_name="requestgroup", null=True, blank=True, on_delete=models.CASCADE)
    request_status = models.IntegerField(default=0)
    #0: for not yet accepted
    #1: accepted
    #2: declined








    

