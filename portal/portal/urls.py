from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('auth/', include('django.contrib.auth.urls')),

    path('', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),
    path('docs/', include('docs.urls', namespace='docs')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
