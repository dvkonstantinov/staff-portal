from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Document(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание документа')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Обновлен')
    file = models.FileField(upload_to='documents/',
                            verbose_name='Файл')
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='documents',
                                 to_field='slug')
    tag = models.ManyToManyField('Tag',
                                 related_name='documents',
                                 blank=True)
    for_signing = models.BooleanField(verbose_name='Нужно ли подписывать',
                                      default=False)
    signed = models.ManyToManyField(User,
                                    related_name='signed_documents',
                                    blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['created_at']


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
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    class Meta:
        unique_together = ['slug', 'parent']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
