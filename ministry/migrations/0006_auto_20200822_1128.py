# Generated by Django 2.2 on 2020-08-22 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0005_pagewordtags'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagewordtags',
            name='rhema_word_for_today',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
