from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from hotels.models import Room

from .forms import BookingForm
from .models import Booking

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@login_required
def create_booking(request, room_id):
    room = get_object_or_404(
        Room,
        id=room_id
    )

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = Booking.objects.create(
                user=request.user,
                room=room,
                check_in=form.cleaned_data['check_in'],
                check_out=form.cleaned_data['check_out'],
                guests=form.cleaned_data['guests'],
                total_price=room.price_per_night,
                status=Booking.STATUS_PENDING
            )

            return render(
                request,
                'bookings/booking_success.html',
                {
                    'booking': booking
                }
            )
    else:
        form = BookingForm()

    return render(
        request,
        'bookings/create_booking.html',
        {
            'room': room,
            'form': form
        }
    )

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    )

    return render(
        request,
        'bookings/my_bookings.html',
        {
            'bookings': bookings
        }
    )

@login_required
def manager_bookings(request):
    if not is_manager(request.user):
        return render(
            request,
            'bookings/access_denied.html'
        )

    bookings = Booking.objects.select_related(
        'user',
        'room',
        'room__hotel'
    ).all()

    return render(
        request,
        'bookings/manager_bookings.html',
        {
            'bookings': bookings
        }
    )