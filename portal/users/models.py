from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
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
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    verified = models.BooleanField(verbose_name="Email Подтвержден",
                                   default=False)
    groups = models.ManyToManyField('Group',
                                    related_name='users',
                                    blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name='Пользователь',
                                related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/full/',
                              default='profile_photos/default/default-avatar.jpg',
                              verbose_name='Фото')
    thumbnail = models.ImageField(upload_to='profile_photos/thumbs/',
                                  default='profile_photos/default/default-avatar.jpg',
                                  verbose_name='Миниатюра')
    job = models.CharField(max_length=300, verbose_name='Должность',
                           blank=True, null=True)
    about = models.TextField(verbose_name='Обо мне', blank=True, null=True)
    personal_email = models.EmailField(verbose_name='Личный email', blank=True,
                                       null=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True,
                                null=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True,
                             null=True)
    telegram = models.CharField(max_length=150, verbose_name='Телеграм',
                                blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Доп. информация'
        verbose_name_plural = 'Доп. информация'


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)

    # @receiver(post_save, sender=User)
    # def create_user_group(sender, instance, created, **kwargs):
    #     if created:
    #         group, _ = Group.objects.get_or_create(
    #             title='Без группы',
    #             slug='none'
    #         )
    #         instance.group = group
    #         instance.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
