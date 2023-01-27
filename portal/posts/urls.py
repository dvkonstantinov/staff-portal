from django.urls import path

from core.decorators import adminuser_required
from posts.views import (AdminPostCategoryView, AdminPostListView,
                         PostListView, category_create, category_edit,
                         category_remove, post_create, post_detail, post_edit,
                         post_remove, tinymce_upload_images)

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('manage/', adminuser_required(AdminPostListView.as_view()),
         name='post_manage'),
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('<int:post_id>/edit/', post_edit, name='post_edit'),
    path('<int:post_id>/remove/', post_remove, name='post_remove'),
    path('manage/upload-images/', tinymce_upload_images,
         name='upload_images'),
    path('category/manage/', adminuser_required(
        AdminPostCategoryView.as_view()), name='category_manage'),
    path('category/create/', category_create, name='category_create'),
    path('category/<slug:slug>/edit/', category_edit, name='category_edit'),
    path('category/<slug:slug>/remove/', category_remove,
         name='category_remove')
]
