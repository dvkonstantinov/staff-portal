from django import forms
from django.contrib.auth import get_user_model

from users.models import Profile, Group

User = get_user_model()

REGISTER_SORT_CHOICES = (
    ('old', 'Сначала старые'),
    ('new', 'Сначала новые'),
)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['job', 'about', 'personal_email', 'birthday', 'phone',
                  'telegram']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 5,
                                           'cols': 40}),
            'birthday': forms.DateInput(format='%d/%m/%Y',
                                        attrs={'type': 'date'})
        }


class UserSearchForm(forms.Form):
    name = forms.CharField(label='Поиск по ФИО', required=False,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'name': 'name'}
                           ))
    registration_date = forms.ChoiceField(label='Дата регистрации',
                                          required=False,
                                          choices=REGISTER_SORT_CHOICES,
                                          widget=forms.Select(
                                              attrs={'class': 'form-select',
                                                     'name': 'date'}
                                          ))
    group = forms.ModelChoiceField(Group.objects.all(),
                                   label='Группа',
                                   required=False,
                                   empty_label='Все',
                                   widget=forms.Select(
                                       attrs={'class': 'form-select',
                                              'name': 'search-group'}
                                   ))


ACTIVITY_SORT_CHOICES = (
    ('', '----------'),
    ('new', 'От нового к старому'),
    ('old', 'От старого к новому'),
)


class AdminUserForm(UserForm):
    groups = forms.ModelMultipleChoiceField(Group.objects.all(),
                                            required=True,
                                            label='Группы',
                                            to_field_name='title',
                                            widget=forms.SelectMultiple(
                                                attrs={'id': 'multiselect',
                                                       'class': 'multiselect'}
                                            ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'groups',
                  'is_admin', 'is_active', 'verified']
        widgets = {
            'is_admin': forms.CheckboxInput(attrs={'class':
                                                       'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class':
                                                        'form-check-input'}),
            'verified': forms.CheckboxInput(attrs={'class':
                                                       'form-check-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AdminUserSearchForm(UserSearchForm):
    email = forms.CharField(label='Поиск по Email', required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'name': 'search-email'}
                            ))
    activity = forms.ChoiceField(label='Дата последнего визита',
                                 required=False,
                                 choices=ACTIVITY_SORT_CHOICES,
                                 widget=forms.Select(
                                     attrs={'class': 'form-select',
                                            'name': 'search-activity'}
                                 ))
    group = forms.ModelChoiceField(Group.objects.all(),
                                   required=False,
                                   label='Группа',
                                   to_field_name='title',
                                   empty_label='Любая',
                                   widget=forms.Select(
                                       attrs={'class': 'form-select',
                                              'name': 'search-group'}
                                   ))

    registration_date = None
    field_order = ['activity', 'group', 'name', 'email']


class AdminGroupEditAddForm(forms.ModelForm):
    title = forms.CharField(label='Название группы',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'name': 'title'}
                            ))

    slug = forms.CharField(label='Slug группы',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'name': 'slug'}
                           ))

    class Meta:
        model = Group
        fields = ['title', 'slug']
