import django_filters
from django.db.models import Q

from posts.models import Post


class PostFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(method='post_content_search')
    category = django_filters.CharFilter(method='post_category_filter')

    def post_content_search(self, queryset, name, value):
        for term in value.split(' '):
            queryset = queryset.filter(Q(title__icontains=term)
                                       | Q(body__icontains=term))
        return queryset

    def post_category_filter(self, queryset, name, value):
        queryset.filter(category__title=value)
        return queryset

    class Meta:
        model: Post


class AdminPostFilter(PostFilter):
    pass
