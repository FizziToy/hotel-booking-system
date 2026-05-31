from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from hotels.models import Hotel, Room

from .models import Booking


class BookingModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='client',
            password='Clientpass123!'
        )

        self.hotel = Hotel.objects.create(
            name='Grand Hotel Kyiv',
            city='Kyiv',
            address='Khreshchatyk 1',
            description='Hotel in city center',
            rating=4.8,
            owner=self.user
        )

        self.room = Room.objects.create(
            hotel=self.hotel,
            title='Deluxe Room',
            description='Room with city view',
            price_per_night=4500,
            capacity=2
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=date(2026, 6, 2),
            check_out=date(2026, 6, 4),
            guests=2,
            total_price=9000,
            status=Booking.STATUS_PENDING
        )

        self.assertEqual(booking.status, Booking.STATUS_PENDING)
        self.assertEqual(booking.room.title, 'Deluxe Room')