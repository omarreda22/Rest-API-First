from rest_framework import serializers
from .models import Guest, Movie, Reservation


class GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["user", "reservation", "name", "mobile"]


class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["pk", "reservation", "guest", "movie"]
