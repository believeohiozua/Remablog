# Generated by Django 2.2 on 2020-08-21 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0004_auto_20200820_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageWordTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('devotion_slide', models.TextField(blank=True, null=True)),
                ('prayer_slide', models.TextField(blank=True, null=True)),
                ('quote_slide', models.TextField(blank=True, null=True)),
                ('training_slide', models.TextField(blank=True, null=True)),
                ('any_other_slide_words1', models.TextField(blank=True, null=True)),
                ('any_other_slide_words2', models.TextField(blank=True, null=True)),
                ('about_us_intro', models.TextField(blank=True, null=True)),
                ('our_mission', models.TextField(blank=True, null=True)),
                ('our_message', models.TextField(blank=True, null=True)),
                ('our_vision', models.TextField(blank=True, null=True)),
                ('special_quotes_intro', models.TextField(blank=True, null=True)),
                ('programme_intro', models.TextField(blank=True, null=True)),
                ('testimony_intro', models.TextField(blank=True, null=True)),
                ('contact_intro', models.TextField(blank=True, null=True)),
                ('contact_address', models.TextField(blank=True, null=True)),
                ('our_social_network_into', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
