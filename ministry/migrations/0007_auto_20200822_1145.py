# Generated by Django 2.2 on 2020-08-22 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0006_auto_20200822_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devotional',
            name='bible_reading',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='devotional',
            name='caption_picture',
            field=models.ImageField(blank=True, null=True, upload_to='devotion'),
        ),
        migrations.AlterField(
            model_name='devotional',
            name='memory_verse',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
