# Generated by Django 3.2 on 2023-04-16 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_auto_20230416_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]