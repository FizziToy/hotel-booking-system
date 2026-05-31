from django.shortcuts import render

from .models import Hotel


def hotel_list(request):
    hotels = Hotel.objects.all()

    return render(
        request,
        'hotels/hotel_list.html',
        {
            'hotels': hotels
        }
    )
from django.shortcuts import get_object_or_404
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(
        Hotel,
        id=hotel_id
    )

    return render(
        request,
        'hotels/hotel_detail.html',
        {
            'hotel': hotel
        }
    )