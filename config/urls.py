from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('hotels/', include('hotels.urls')),
    path('bookings/', include('bookings.urls')),
    path('ai/', include('ai_assistant.urls')),
]