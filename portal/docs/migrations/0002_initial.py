# Generated by Django 4.1.1 on 2023-01-26 22:41

import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='documents', to='docs.category', to_field='slug'),
        ),
        migrations.AddField(
            model_name='document',
            name='groups',
            field=models.ManyToManyField(related_name='allowed_documents', to='users.group'),
        ),
        migrations.AddField(
            model_name='document',
            name='signed',
            field=models.ManyToManyField(blank=True, related_name='signed_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='documents', to='docs.tag'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='docs.category'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('slug', 'parent')},
        ),
    ]
