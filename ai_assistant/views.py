import os

from django.shortcuts import render
from openai import OpenAI

from hotels.models import Room


def ai_recommendation(request):
    answer = None

    if request.method == 'POST':
        user_prompt = request.POST.get('prompt')

        rooms = Room.objects.select_related('hotel').all()

        rooms_text = ''

        for room in rooms:
            rooms_text += (
                f"Готель: {room.hotel.name}, "
                f"місто: {room.hotel.city}, "
                f"номер: {room.title}, "
                f"ціна: {room.price_per_night} грн, "
                f"місткість: {room.capacity} гостей. "
            )

        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )

        try:
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        'role': 'system',
                        'content': (
                            'Ти AI-помічник системи бронювання готелів. '
                            'Рекомендуй користувачу тільки ті готелі та номери, '
                            'які є в переданому списку.'
                        )
                    },
                    {
                        'role': 'user',
                        'content': (
                            f"Доступні номери: {rooms_text}\n\n"
                            f"Запит користувача: {user_prompt}"
                        )
                    }
                ]
            )

            answer = response.choices[0].message.content

        except Exception:
            answer = (
                'AI-сервіс тимчасово недоступний або перевищено квоту API. '
                'Для демонстрації: рекомендую переглянути доступні номери у списку готелів.'
            )

    return render(
        request,
        'ai_assistant/recommendation.html',
        {
            'answer': answer
        }
    )