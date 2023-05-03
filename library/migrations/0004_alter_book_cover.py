# Generated by Django 4.2 on 2023-05-03 17:49

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[300, 400], upload_to='covers', verbose_name='Viršelis'),
        ),
    ]
