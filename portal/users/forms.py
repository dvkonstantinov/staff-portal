from django import forms
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()


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
