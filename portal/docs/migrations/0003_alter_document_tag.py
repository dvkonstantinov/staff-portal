# Generated by Django 4.1.1 on 2022-10-31 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0002_document_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='tag',
            field=models.ManyToManyField(null=True, related_name='documents', to='docs.tag'),
        ),
    ]
