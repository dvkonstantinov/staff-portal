from django.urls import path

from docs.views import doc_list, doc_create, doc_detail, doc_edit, \
    category_list, category_create, category_detail, category_edit, tag_list, \
    tag_create, tag_detail, tag_edit

app_name = 'docs'

urlpatterns = [
    path('', doc_list, name='doc_list'),
    path('create/', doc_create, name='doc_create'),
    path('<int:doc_id>', doc_detail, name='doc_detail'),
    path('<int:doc_id>/edit', doc_edit, name='doc_edit'),
    path('category/', category_list, name='category_list'),
    path('category/create/', category_create, name='category_create'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('category/<slug:slug>/edit/', category_edit, name='category_edit'),
    path('tags/', tag_list, name='tag_list'),
    path('tags/create/', tag_create, name='tag_create'),
    path('tags/<slug:slug>', tag_detail, name='tag_detail'),
    path('tags/<slug:slug>/edit/', tag_edit, name='tag_edit'),
]
