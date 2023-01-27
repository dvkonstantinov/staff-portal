from django.urls import path

from core.decorators import adminuser_required
from users.views import (AdminGroupListView, AdminUserListView, UserListView,
                         admin_group_add, admin_group_edit, admin_group_remove,
                         admin_user_profile, remove_avatar, upload_avatar,
                         user_profile)

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:user_id>/', user_profile, name='user_profile'),
    path('ajax/makeavatar/', upload_avatar, name='upload_avatar'),
    path('ajax/removeavatar/', remove_avatar, name='remove_avatar'),
    path('manage/', adminuser_required(AdminUserListView.as_view()),
         name='user_manage'),
    path('manage/<int:user_id>/', admin_user_profile, name='user_edit'),
    path('groups/', adminuser_required(AdminGroupListView.as_view()),
         name='group_manage'),
    path('groups/<int:group_id>/', admin_group_edit, name='group_edit'),
    path('groups/<int:group_id>/remove/', admin_group_remove,
         name='group_remove'),
    path('groups/new/', admin_group_add, name='group_add'),
]
