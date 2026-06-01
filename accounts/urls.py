from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'verify-email/<uidb64>/<token>/',
        views.verify_email,
        name='verify_email'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'profile/',
        views.profile,
        name='profile'
),
]