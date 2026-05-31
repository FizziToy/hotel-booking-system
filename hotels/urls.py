from django.urls import path

from . import views

app_name = "hotels"

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),

    path(
        '<int:hotel_id>/',
        views.hotel_detail,
        name='hotel_detail'
    ),
]