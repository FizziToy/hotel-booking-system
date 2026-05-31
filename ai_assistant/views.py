import requests

from django.shortcuts import render

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

        prompt = (
            'Ти AI-помічник системи бронювання готелів. '
            'Рекомендуй користувачу тільки ті готелі та номери, '
            'які є в списку.\n\n'
            f'Доступні номери: {rooms_text}\n\n'
            f'Запит користувача: {user_prompt}'
        )

        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.2',
                    'prompt': prompt,
                    'stream': False
                },
                timeout=120
            )

            data = response.json()
            answer = data.get('response')

        except Exception:
            answer = (
                'Локальний AI-сервіс Ollama недоступний. '
                'Перевірте, чи запущена Ollama та модель llama3.2.'
            )

    return render(
        request,
        'ai_assistant/recommendation.html',
        {
            'answer': answer
        }
    )