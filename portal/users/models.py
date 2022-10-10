from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from portal.settings import AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('Email обязательно нужно указать')
        email = self.normalize_email(email)
        username = email.split('@')[0].replace('.', '-')
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        # null=True,
        blank=False,
        help_text=_(
            'Имя пользователя не должно превышать 150 символов, '
            'из спецсимволов разрешены только @/./+/-/_ '),
        validators=[username_validator],
        error_messages={
            'unique': _("Имя пользователя уже существует"),
        }
    )
    email = models.EmailField(
        _('Адрес эл. почты'),
        unique=True,
        blank=False,
        max_length=150,
        error_messages={
            'unique': _("Такой Email уже зарегистрирован"),
        }
    )
    password = models.CharField(_('Пароль'), max_length=150)
    first_name = models.CharField(_('Имя'), max_length=150)
    last_name = models.CharField(_('Фамилия'), max_length=150)
    patronymic = models.CharField(_('Отчество'), max_length=150, null=True,
                                  blank=True)
    is_staff = models.BooleanField(_('Статус модератора'), default=False)
    is_admin = models.BooleanField(_('Права администратора'), default=False)
    is_active = models.BooleanField(_('Активный пользователь'), default=True)
    last_activity = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'patronymic']

    objects = CustomUserManager()

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    verified = models.BooleanField(verbose_name="Подтвержден", default=False)
