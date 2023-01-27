from django import forms
from django.conf import settings
from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, UserCreationForm)
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from authapp.utils import check_email_pattern

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='Имя',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'name': 'first_name',
                                            'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=150, required=True,
                                label='Фамилия',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'name': 'last_name'}))
    patronymic = forms.CharField(max_length=150, required=False,
                                 label='Отчество',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'name': 'patronymic'}))
    email = forms.EmailField(max_length=254, label='Email @ilaaspect.com',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'name': 'email'}))
    password1 = forms.CharField(
        max_length=30, required=True, label='Пароль',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': "password1",
                   'type': "password"}),
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(max_length=30, required=True,
                                label='Подтверждение пароля',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'name': "password2",
                                           'type': "password"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not check_email_pattern(email):
            raise ValidationError("Может быть зарегистрирован только email "
                                  "@ilaaspect.com")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Такой email уже зарегистрирован")
        return email

    def save(self, commit=True):
        username = self.cleaned_data['email'].split('@')[0]
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
                                           'autofocus': True}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }))

    field_order = ['username', 'password']

    error_messages = {
        "invalid_login": _(
            "Введите правильный адрес электронной почты и пароль."
        ),
        "inactive": _("Этот аккаунт неактивный."),
        "unconfirmed_email": _("Ваш Email не подтвержден. Перейдите по "
                               "ссылке из почты, чтобы его подтвердить"),
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:

            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            print(self.user_cache)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
                self.confirm_verify_email(self.user_cache)

        return self.cleaned_data

    def confirm_verify_email(self, user):
        if not user.verified:
            raise ValidationError(
                self.error_messages["unconfirmed_email"],
                code="unconfirmed_email",
            )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Старый пароль"),
        strip=False,
        widget=forms.PasswordInput(),
    )
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        strip=False,
        widget=forms.PasswordInput(),
    )
    field_order = ['old_password', 'new_password1', 'new_password2']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Адрес электронной почты", max_length=254,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'name': 'email'}))

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        email = self.cleaned_data["email"]
        site_name = settings.SITE_DOMAIN
        domain = settings.SITE_DOMAIN
        email_field_name = User.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": settings.SITE_PROTOCOL,
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )
