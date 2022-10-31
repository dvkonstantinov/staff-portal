from django.urls import path

from core.decorators import adminuser_required
from users.views import user_profile, upload_avatar, remove_avatar, \
    UserListView, AdminUserListView, admin_user_profile, AdminGroupListView, \
    admin_group_edit, admin_group_add

app_name = 'users'

urlpatterns = [
    path('<int:user_id>/', user_profile, name='user_profile'),
    path('', UserListView.as_view(), name='user_list'),
    path('ajax/makeavatar/', upload_avatar, name='upload_avatar'),
    path('ajax/removeavatar/', remove_avatar, name='remove_avatar'),
    path('users/', adminuser_required(AdminUserListView.as_view()),
         name='user_manage'),
    path('users/<int:user_id>/', admin_user_profile, name='user_edit'),
    path('groups/', adminuser_required(AdminGroupListView.as_view()),
         name='group_manage'),
    path('groups/<int:group_id>/', admin_group_edit, name='group_edit'),
    path('groups/new/', admin_group_add, name='group_add'),
]
