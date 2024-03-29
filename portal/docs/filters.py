import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class DocFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='doc_title_search')
    add_date = django_filters.CharFilter(method='sort')
    status = django_filters.CharFilter(method='status_search')
    category = django_filters.CharFilter(lookup_expr='exact')

    def doc_title_search(self, queryset, name, value):
        queryset = queryset.filter(title__icontains=value)
        return queryset

    def sort(self, queryset, name, value):
        if value == 'new':
            queryset = queryset.order_by('-id')
            return queryset
        return queryset

    def status_search(self, queryset, name, value):
        if value == 'all':
            return queryset
        elif value == 'signed':
            queryset = queryset.filter(signed=self.request.user,
                                       for_signing=True)
            return queryset
        elif value == 'unsigned':
            queryset = queryset.filter(~Q(signed=self.request.user),
                                       for_signing=True)
            return queryset
        elif value == 'to-view':
            queryset = queryset.filter(for_signing=False)
            return queryset


class CategoryFilter(django_filters.FilterSet):
    pass
