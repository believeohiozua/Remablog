# Generated by Django 2.2 on 2020-08-21 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subscribe', models.BooleanField(default=True)),
            ],
        ),
    ]
