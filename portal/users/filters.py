import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='search_name')
    registration_date = django_filters.CharFilter(method='register_sort')
    group = django_filters.CharFilter(method='filter_group')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'registration_date', 'group',
                  'email']

    def search_name(self, queryset, name, value):
        for term in value.split(' '):
            queryset = queryset.filter(Q(first_name__icontains=term)
                                       | Q(last_name__icontains=term)
                                       | Q(patronymic__icontains=term)
                                       | Q(email__icontains=term))
        return queryset

    def register_sort(self, queryset, name, value):
        if value == 'new':
            queryset = queryset.order_by('-date_joined')
            return queryset
        elif value == 'old':
            queryset = queryset.order_by('date_joined')
            return queryset
        return queryset

    def filter_group(self, queryset, name, value):
        print(queryset)
        queryset = queryset.filter(groups__slug=value)
        print(queryset)
        return queryset


class AdminUserFilter(UserFilter):
    activity = django_filters.CharFilter(method='activity_sort')
    group = django_filters.CharFilter(method='group_filter')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def activity_sort(self, queryset, name, value):
        if value == 'new':
            queryset = queryset.order_by('-last_activity')
            return queryset
        queryset = queryset.order_by('last_activity')
        return queryset

    def group_filter(self, queryset, name, value):
        if value == 'none':
            queryset = queryset.filter(groups=None)
            return queryset
        elif value == 'all':
            return queryset
        else:
            queryset = queryset.filter(groups__slug=value)
            return queryset
