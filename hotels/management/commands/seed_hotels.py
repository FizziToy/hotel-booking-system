from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from hotels.models import Hotel, Room


class Command(BaseCommand):
    help = 'Creates demo hotels and rooms'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        owner, _ = User.objects.get_or_create(
            username='demo_manager',
            defaults={
                'email': 'manager@example.com',
                'is_staff': True
            }
        )

        owner.set_password('DemoManager123!')
        owner.save()

        hotels_data = [
            {
                'name': 'Grand Hotel Kyiv',
                'city': 'Київ',
                'address': 'вул. Хрещатик, 1',
                'description': 'Розкішний готель у центрі Києва з преміальними номерами.',
                'rooms': [
                    ('Deluxe Room', 'Просторий номер з видом на місто.', 4500, 2),
                    ('Premium Suite', 'Люкс із вітальнею та великим ліжком.', 7200, 3),
                    ('Business Room', 'Зручний номер для ділових поїздок.', 3900, 1),
                ],
            },
            {
                'name': 'Lviv Royal Residence',
                'city': 'Львів',
                'address': 'пл. Ринок, 12',
                'description': 'Атмосферний готель у старовинному центрі Львова.',
                'rooms': [
                    ('Classic Room', 'Затишний номер у класичному стилі.', 2800, 2),
                    ('Royal Suite', 'Просторий люкс з історичним інтер’єром.', 6100, 3),
                    ('Family Room', 'Номер для родини з двома спальними зонами.', 5200, 4),
                ],
            },
            {
                'name': 'Odesa Sea View Hotel',
                'city': 'Одеса',
                'address': 'Французький бульвар, 25',
                'description': 'Сучасний готель біля моря з панорамними краєвидами.',
                'rooms': [
                    ('Sea View Room', 'Номер з видом на море.', 4800, 2),
                    ('Junior Suite', 'Комфортний напівлюкс для відпочинку.', 5900, 3),
                    ('Economy Room', 'Бюджетний номер для коротких подорожей.', 2200, 2),
                ],
            },
            {
                'name': 'Carpathian Forest Resort',
                'city': 'Яремче',
                'address': 'вул. Гірська, 7',
                'description': 'Готель серед Карпат для спокійного відпочинку на природі.',
                'rooms': [
                    ('Mountain Room', 'Номер з видом на гори.', 3500, 2),
                    ('Wooden Chalet', 'Окремий дерев’яний будиночок.', 7800, 4),
                    ('Standard Room', 'Затишний стандартний номер.', 2600, 2),
                ],
            },
            {
                'name': 'Kharkiv Business Palace',
                'city': 'Харків',
                'address': 'просп. Науки, 18',
                'description': 'Готель бізнес-класу з комфортними умовами для роботи.',
                'rooms': [
                    ('Business Standard', 'Номер для робочих поїздок.', 3100, 1),
                    ('Conference Suite', 'Люкс для гостей ділових заходів.', 6500, 2),
                    ('Twin Room', 'Номер з двома окремими ліжками.', 3700, 2),
                ],
            },
        ]

        for hotel_data in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults={
                    'city': hotel_data['city'],
                    'address': hotel_data['address'],
                    'description': hotel_data['description'],
                    'rating': 0,
                    'owner': owner,
                }
            )

            for title, description, price, capacity in hotel_data['rooms']:
                Room.objects.get_or_create(
                    hotel=hotel,
                    title=title,
                    defaults={
                        'description': description,
                        'price_per_night': price,
                        'capacity': capacity,
                        'is_available': True,
                    }
                )

        self.stdout.write(
            self.style.SUCCESS('Demo hotels and rooms were created successfully.')
        )