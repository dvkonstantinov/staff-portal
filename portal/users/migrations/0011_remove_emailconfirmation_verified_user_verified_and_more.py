# Generated by Django 4.1.1 on 2022-10-18 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailconfirmation',
            name='verified',
        ),
        migrations.AddField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Email Подтвержден'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='profile_photos/full/default.jpg', upload_to='profile_photos/full/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='thumbnail',
            field=models.ImageField(default='profile_photos/thumbs/default.jpg', upload_to='profile_photos/thumbs/', verbose_name='Миниатюра'),
        ),
    ]
