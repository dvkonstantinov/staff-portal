from django.urls import path
from .views import main_page

app_name = 'main'

urlpatterns = [
    path('', main_page, name='home_page'),
]
