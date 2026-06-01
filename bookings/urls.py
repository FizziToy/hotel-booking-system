from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path(
        'create/<int:room_id>/',
        views.create_booking,
        name='create_booking'
    ),

    path(
        'my/',
        views.my_bookings,
        name='my_bookings'
    ),

    path(
        'manager/',
        views.manager_bookings,
        name='manager_bookings'
    ),

    path(
    'manager/<int:booking_id>/confirm/',
    views.confirm_booking,
    name='confirm_booking'
    ),

    path(
        'manager/<int:booking_id>/cancel/',
        views.cancel_booking,
        name='cancel_booking'
    ),
    path(
    'cancel/<int:booking_id>/',
    views.cancel_my_booking,
    name='cancel_my_booking'
    ),
]