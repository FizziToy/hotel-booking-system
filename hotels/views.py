from django.db.models import Avg
from django.shortcuts import get_object_or_404, render

from .models import Hotel


def hotel_list(request):
    hotels = Hotel.objects.annotate(
        average_rating=Avg('reviews__rating')
    )

    return render(
        request,
        'hotels/hotel_list.html',
        {
            'hotels': hotels
        }
    )


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(
        Hotel.objects.annotate(
            average_rating=Avg('reviews__rating')
        ),
        id=hotel_id
    )

    reviews = hotel.reviews.select_related(
        'user'
    ).all()

    return render(
        request,
        'hotels/hotel_detail.html',
        {
            'hotel': hotel,
            'reviews': reviews
        }
    )