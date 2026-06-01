from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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

    confirmed_bookings = Booking.objects.filter(
        room=room,
        status=Booking.STATUS_CONFIRMED
    ).values(
        'check_in',
        'check_out'
    )

    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)

        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            nights = (check_out - check_in).days

            overlapping_booking_exists = Booking.objects.filter(
                room=room,
                status=Booking.STATUS_CONFIRMED,
                check_in__lt=check_out,
                check_out__gt=check_in
            ).exists()

            if nights <= 0:
                form.add_error(
                    'check_out',
                    'Дата виїзду має бути пізніше дати заїзду.'
                )

            elif overlapping_booking_exists:
                form.add_error(
                    'check_in',
                    'На обрані дати цей номер уже заброньований.'
                )

            else:
                total_price = room.price_per_night * nights

                booking = Booking.objects.create(
                    user=request.user,
                    room=room,
                    check_in=check_in,
                    check_out=check_out,
                    guests=form.cleaned_data['guests'],
                    total_price=total_price,
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
        form = BookingForm(room=room)

    return render(
        request,
        'bookings/create_booking.html',
        {
            'room': room,
            'form': form,
            'confirmed_bookings': list(confirmed_bookings)
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


@login_required
def confirm_booking(request, booking_id):
    if not is_manager(request.user):
        return render(
            request,
            'bookings/access_denied.html'
        )

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    booking.status = Booking.STATUS_CONFIRMED
    booking.save()

    return redirect('bookings:manager_bookings')


@login_required
def cancel_booking(request, booking_id):
    if not is_manager(request.user):
        return render(
            request,
            'bookings/access_denied.html'
        )

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    booking.status = Booking.STATUS_CANCELLED
    booking.save()

    return redirect('bookings:manager_bookings')


@login_required
def cancel_my_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    booking.status = Booking.STATUS_CANCELLED
    booking.save()

    return redirect('bookings:my_bookings')