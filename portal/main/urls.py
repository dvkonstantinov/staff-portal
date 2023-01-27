from django.urls import path, re_path

from .views import main_page, protected_media

app_name = 'main'

urlpatterns = [
    path('', main_page, name='home_page'),
    re_path(r'^media/', protected_media, name='protected_media')
]
