# Generated by Django 2.2 on 2020-09-05 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0013_auto_20200904_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
