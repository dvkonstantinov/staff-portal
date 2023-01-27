from django.urls import path

from core.decorators import adminuser_required
from docs.views import (AdminCategoryListView, AdminDocListView, DocListView,
                        category_create, category_edit, category_remove,
                        doc_create, doc_detail, doc_edit, doc_remove, doc_sign,
                        doc_signers)

app_name = 'docs'

urlpatterns = [
    path('', DocListView.as_view(), name='doc_list'),
    path('manage/', adminuser_required(AdminDocListView.as_view()),
         name='docs_manage'),
    path('create/', doc_create, name='doc_create'),
    path('<int:doc_id>/', doc_detail, name='doc_detail'),
    path('sign', doc_sign, name='doc_sign'),
    path('<int:doc_id>/edit/', doc_edit, name='doc_edit'),
    path('<int:doc_id>/remove/', doc_remove, name='doc_remove'),
    path('<int:doc_id>/signers/', doc_signers, name='doc_signers'),
    # path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/manage/',
         adminuser_required(AdminCategoryListView.as_view()),
         name='category_manage'),
    path('category/create/', category_create, name='category_create'),
    # path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('category/<slug:slug>/edit/', category_edit, name='category_edit'),
    path('category/<slug:slug>/remove/', category_remove,
         name='category_remove'),
    # path('tags/', tag_list, name='tag_list'),
    # path('tags/create/', tag_create, name='tag_create'),
    # path('tags/<slug:slug>/', tag_detail, name='tag_detail'),
    # path('tags/<slug:slug>/edit/', tag_edit, name='tag_edit'),
]
