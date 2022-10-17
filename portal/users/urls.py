from django.urls import path

from users.views import user_profile, upload_avatar, remove_avatar, user_list

app_name = 'users'

urlpatterns = [
    path('<int:user_id>/', user_profile, name='user_profile'),
    path('', user_list, name='user_list'),
    path('ajax/makeavatar/', upload_avatar, name='upload_avatar'),
    path('ajax/removeavatar/', remove_avatar, name='remove_avatar'),
]
