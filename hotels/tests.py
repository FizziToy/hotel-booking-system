from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Hotel, Room


class HotelRoomModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpass123!'
        )

        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            city='Kyiv',
            address='Test address',
            description='Test description',
            rating=4.5,
            owner=self.user
        )

    def test_hotel_creation(self):
        self.assertEqual(str(self.hotel), 'Test Hotel')

    def test_room_creation(self):
        room = Room.objects.create(
            hotel=self.hotel,
            title='Standard Room',
            description='Test room',
            price_per_night=1500,
            capacity=2
        )

        self.assertEqual(str(room), 'Test Hotel - Standard Room')