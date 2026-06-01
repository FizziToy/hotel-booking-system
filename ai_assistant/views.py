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

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def ai_chat_api(request):
    if request.method != 'POST':
        return JsonResponse(
            {
                'answer': 'Метод не підтримується.'
            },
            status=405
        )

    data = json.loads(request.body)

    user_prompt = data.get('message', '')

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
            "Ти AI-помічник системи бронювання готелів. "
            "Використовуй лише інформацію про номери, яку отримав. "
            "Не вигадуй ціни, міста або характеристики. "
            "Якщо номер відповідає бюджету користувача, скажи що він підходить. "
            "Якщо не відповідає — поясни чому. "
            "Відповідай українською мовою.\n\n"

            f"Доступні номери: {rooms_text}\n\n"

            f"Запит користувача: {user_prompt}"
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

        result = response.json()

        answer = result.get(
            'response',
            'Не вдалося отримати відповідь AI.'
        )

    except Exception:
        answer = (
            'AI-помічник зараз недоступний. '
            'Перевірте, чи запущена Ollama.'
        )

    return JsonResponse(
        {
            'answer': answer
        }
    )