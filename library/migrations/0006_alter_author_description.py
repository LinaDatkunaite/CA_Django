# Generated by Django 4.2 on 2023-05-09 17:52

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_bookinstance_reader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
