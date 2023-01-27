from django.contrib.auth import get_user_model
from django.db import models
from tinymce.models import HTMLField

from users.models import Group

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название',
                             db_index=True)
    body = HTMLField(db_index=True, verbose_name='Текст поста')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Обновлен')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               verbose_name='Автор')
    is_published = models.BooleanField(default=False,
                                       verbose_name='Опубликовать')
    is_for_deleting = models.BooleanField(default=False,
                                          verbose_name='Удалено')
    image = models.ImageField(upload_to='posts/preview/',
                              verbose_name='Превью фото', null=True)
    groups = models.ManyToManyField(Group,
                                    related_name='allowed_posts',
                                    verbose_name='Группы пользователей',
                                    help_text='Каким группам пользователей '
                                              'доступен пост')
    category = models.ForeignKey('PostCategory',
                                 verbose_name='Рубрика',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    @staticmethod
    def get_posts_for_current_user(user):
        return Post.objects.filter(is_for_deleting=False,
                                   groups__in=user.groups.all()
                                   ).distinct()


class PostCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название рубрики')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рубрика новости'
        verbose_name_plural = 'Рубрики новостей'
