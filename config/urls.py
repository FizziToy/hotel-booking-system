from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('hotels/', include('hotels.urls')),
    path('bookings/', include('bookings.urls')),
    path('ai/', include('ai_assistant.urls')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )