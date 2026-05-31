from django.conf import settings
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    address = models.TextField()

    description = models.TextField()

    rating = models.FloatField(default=0)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotels'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    capacity = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel.name} - {self.title}'