# Generated by Django 2.2 on 2020-08-20 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(help_text='subject', max_length=100)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Devotional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(blank=True, null=True)),
                ('bible_reading', models.CharField(max_length=200)),
                ('memory_verse', models.CharField(max_length=200)),
                ('devotion', tinymce.models.HTMLField()),
                ('caption_picture', models.ImageField(upload_to='devotion')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('prog_image', models.ImageField(upload_to='programme_image')),
                ('overview', models.TextField()),
                ('detail', tinymce.models.HTMLField()),
                ('_type', models.CharField(choices=[('course', 'course'), ('seminar', 'seminar'), ('workshop', 'workshop'), ('Ministry', 'Ministry')], default='course', max_length=10)),
                ('duration_from', models.DateField()),
                ('duration_to', models.DateField()),
                ('slug', models.SlugField(blank=True, null=True)),
                ('publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('next_programme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='ministry.Programme')),
                ('post_tag', models.ManyToManyField(blank=True, to='ministry.PostTag')),
                ('previous_programme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='ministry.Programme')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Testimony',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.CharField(max_length=200)),
                ('phone_number', models.CharField(help_text='phone number', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('your_testimony', models.TextField()),
                ('add_a_photo', models.ImageField(blank=True, null=True, upload_to='Testimony_image')),
                ('publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('next_testimony', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='ministry.Testimony')),
                ('previous_testimony', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='ministry.Testimony')),
            ],
        ),
        migrations.CreateModel(
            name='TestimonyReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.CharField(max_length=200)),
                ('phone_number', models.CharField(help_text='phone number', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('content', models.TextField()),
                ('reply', models.TextField(blank=True, null=True)),
                ('replyed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('testimony', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testimony_reviews', to='ministry.Testimony')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='quotes')),
                ('quote', models.TextField()),
                ('publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammeReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.CharField(max_length=200)),
                ('phone_number', models.CharField(help_text='phone number', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('content', models.TextField()),
                ('reply', models.TextField(blank=True, null=True)),
                ('replyed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('programme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme_reviews', to='ministry.Programme')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.CharField(max_length=200)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_photo', models.ImageField(upload_to='profile')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited', models.CharField(blank=True, max_length=200, null=True)),
                ('devotional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ministry.Devotional')),
                ('programme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ministry.Programme')),
                ('quote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ministry.Quote')),
                ('testimony', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ministry.Testimony')),
            ],
        ),
        migrations.CreateModel(
            name='DevotionalReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_names', models.CharField(max_length=200)),
                ('phone_number', models.CharField(help_text='phone number', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('content', models.TextField()),
                ('reply', models.TextField(blank=True, null=True)),
                ('replyed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('devotional', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devotional_reviews', to='ministry.Devotional')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
