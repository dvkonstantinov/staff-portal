from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    PasswordChangeForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='Имя',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'name': 'first_name',
                                            'placeholder': 'Иван',
                                            'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=150, required=True,
                                label='Фамилия',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'name': 'last_name',
                                           'placeholder': 'Иванов'}))
    patronymic = forms.CharField(max_length=150, required=True,
                                 label='Отчество',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'name': 'patronymic',
                                            'placeholder': 'Иванович'}))
    email = forms.EmailField(max_length=254, label='Email @ilaaspect.com',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'name': 'email',
                                        'placeholder':
                                            'ivanov@ilaaspect.com'}))
    password1 = forms.CharField(max_length=30, required=True, label='Пароль',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'name': "password1",
                                           'type': "password",
                                           'placeholder': 'pass'}),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(max_length=30, required=True,
                                label='Подтверждение пароля',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'name': "password2",
                                           'type': "password",
                                           'placeholder': 'pass'}))

    def save(self, commit=True):
        username = self.cleaned_data['email'].split('@')[0].replace('.', '-')
        user = super().save(commit=False)
        user.username = username
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'email']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, label='Email @ilaaspect.com',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'name': 'email',
                                           'placeholder': 'ivanov@ilaaspect.com',
                                           'autofocus': True}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'pass',
        }))
    field_order = ['username', 'password']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Старый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,
                                          'placeholder': 'oldpass'}),
    )
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(attrs={'placeholder': 'newpass'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Новый пароль, еще раз"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'newpass'}),
    )
    field_order = ['old_password', 'new_password1', 'new_password2']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Адрес электронной почты", max_length=254,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'name': 'email',
                                        'placeholder':
                                            'ivanov@ilaaspect.com'}))

