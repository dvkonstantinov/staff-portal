import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='fio_search')
    registration_date = django_filters.CharFilter(method='register_sort')


    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def fio_search(self, queryset, name, value):
        for term in value.split(' '):
            queryset = queryset.filter(Q(first_name__icontains=term) |
                                       Q(last_name__icontains=term) |
                                       Q(patronymic__icontains=term))
        return queryset

    def register_sort(self, queryset, name, value):
        if value == 'new':
            queryset = queryset.order_by('-date_joined')
            return queryset
        return queryset
