from django.db import models
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL

# Guest - Movie - Reservation


class Guest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()

    def __str__(self):
        return self.name

    def get_put_url(self):
        # return f'/rest_one/{self.id}/'
        return '/rest_get/'


class Movie(models.Model):
    name = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    data = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='reservation', on_delete=models.CASCADE)

    def __str__(self):
        return self.guest.name
