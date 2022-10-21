from django import forms
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()

REGISTER_SORT_CHOICES = (
    ('old', 'Сначала старые'),
    ('new', 'Сначала новые'),
)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic']


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
