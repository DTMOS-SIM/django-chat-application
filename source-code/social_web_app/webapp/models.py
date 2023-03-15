from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.CharField(max_length=256, null=False, blank=False)
    gender = models.CharField(max_length=1, null=False, blank=False)
    friend = models.ManyToManyField("self")

    def __unicode__(self):
        return self.user.username


class Images(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.ImageField(null=False, blank=False)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=256, null=False, blank=False)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Chats(models.Model):
    message = models.CharField(max_length=256, null=False, blank=False)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=False, blank=False)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name