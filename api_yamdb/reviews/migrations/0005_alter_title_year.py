# Generated by Django 3.2 on 2023-04-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_title_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(verbose_name='Год выхода'),
        ),
    ]
