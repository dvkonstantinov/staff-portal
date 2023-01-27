from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from users.models import Group

User = get_user_model()


class Document(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название',
                             db_index=True)
    description = models.TextField(verbose_name='Описание документа')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Обновлен')
    file = models.FileField(upload_to='documents/',
                            verbose_name='Файл')
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 related_name='documents',
                                 to_field='slug',
                                 blank=True,
                                 null=True)
    tag = models.ManyToManyField('Tag',
                                 related_name='documents',
                                 blank=True)
    for_signing = models.BooleanField(verbose_name='Нужно ли подписывать',
                                      default=False)
    groups = models.ManyToManyField(Group,
                                    related_name='allowed_documents')
    signed = models.ManyToManyField(User,
                                    related_name='signed_documents',
                                    blank=True)
    is_for_deleting = models.BooleanField(verbose_name='Помечен на удаление',
                                          default=False)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['created_at']

    def __str__(self):
        return self.title

    @staticmethod
    def get_docs_for_current_user(user):
        return Document.objects.filter(is_for_deleting=False,
                                       groups__in=user.groups.all()
                                       ).distinct()


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']


class Category(MPTTModel):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ['slug', 'parent']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
