# Generated by Django 2.2 on 2020-08-21 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0003_auto_20200820_2155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletter',
            old_name='email',
            new_name='sub_email',
        ),
    ]