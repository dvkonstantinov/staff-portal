from django import forms
from django.contrib.auth import get_user_model

from users.models import Group, Profile

User = get_user_model()

REGISTER_SORT_CHOICES = (
    ('new', 'Сначала новые'),
    ('old', 'Сначала старые'),
)

ACTIVITY_SORT_CHOICES = (
    ('', '----------'),
    ('new', 'От нового к старому'),
    ('old', 'От старого к новому'),
)


def get_groups_with_nonegroup():
    groups = Group.objects.all()
    choice_list = [('all', 'Все'), ('none', 'Без группы')]
    for gr in groups:
        choice_list.append((gr.slug, gr.title))
    return choice_list


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
    name = forms.CharField(
        label='ФИО, Email', required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'search-name'}
        ))
    registration_date = forms.ChoiceField(
        label='Дата регистрации',
        required=False,
        choices=REGISTER_SORT_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select',
                   'name': 'search-date'}
        ))
    group = forms.ModelChoiceField(
        Group.objects.all(),
        label='Группа',
        required=False,
        to_field_name='slug',
        empty_label='Все',
        widget=forms.Select(
            attrs={'class': 'form-select',
                   'name': 'search-group'}
        ))


class AdminUserForm(UserForm):
    groups = forms.ModelMultipleChoiceField(
        Group.objects.all(),
        required=True,
        label='Группы',
        to_field_name='title',
        widget=forms.SelectMultiple(
            attrs={'id': 'multiselect',
                   'class': 'multiselect'}
        ))
    email = forms.CharField(
        label='Email',
        required=True,
        disabled=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'email'}
        ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'groups',
                  'is_admin', 'is_active', 'verified']
        widgets = {
            'is_admin': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
            'verified': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AdminUserSearchForm(UserSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        custom_query = get_groups_with_nonegroup()
        self.fields['group'] = forms.ChoiceField(
            choices=custom_query,
            required=True,
            label='Группа',
            widget=forms.Select(
                attrs={'class': 'form-select'}
            ))

    activity = forms.ChoiceField(
        label='Дата последнего визита',
        required=False,
        choices=ACTIVITY_SORT_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select',
                   'name': 'search-activity'}
        ))

    registration_date = None
    field_order = ['name', 'group', 'activity']


class AdminGroupEditAddForm(forms.ModelForm):
    title = forms.CharField(
        label='Название группы',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'title'}
        ))

    slug = forms.CharField(
        label='Slug группы',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'slug'}
        ))

    class Meta:
        model = Group
        fields = ['title', 'slug']
