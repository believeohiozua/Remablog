from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce import HTMLField
from django.template.defaultfilters import slugify
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class PostView(models.Model):
    visited = models.CharField(max_length=200, blank=True, null=True)
    quote = models.ForeignKey(
        'Quote', blank=True, null=True, on_delete=models.CASCADE)
    programme = models.ForeignKey(
        'Programme', null=True, on_delete=models.CASCADE)
    devotional = models.ForeignKey(
        'Devotional', blank=True, null=True, on_delete=models.CASCADE)
    testimony = models.ForeignKey(
        'Testimony', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.visited)

    def save(self, *args, **kwargs):
        if self.quote:
            self.visited = self.quote
        elif self.programme:
            self.visited = self.programme
        elif self.devotional:
            self.visited = self.devotional
        elif self.testimony:
            self.visited = self.testimony
        else:
            self.visited = "unknown"
        super(PostView, self).save(*args, **kwargs)


class ProgrammeReview(models.Model):
    full_names = models.CharField(max_length=200)
    phone_number = models.CharField(help_text='phone number', max_length=20)
    email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    programme = models.ForeignKey(
        'Programme', related_name='programme_reviews', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reply = models.TextField(blank=True, null=True)
    replyed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.full_names + " on " + self.programme)


class DevotionalReview(models.Model):
    full_names = models.CharField(max_length=200)
    phone_number = models.CharField(help_text='phone number', max_length=20)
    email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    devotional = models.ForeignKey(
        'Devotional', related_name='devotional_reviews', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reply = models.TextField(blank=True, null=True)
    replyed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.full_names + "'s Review on " + str(self.devotional))


class TestimonyReview(models.Model):
    full_names = models.CharField(max_length=200)
    phone_number = models.CharField(help_text='phone number', max_length=20)
    email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    testimony = models.ForeignKey(
        'Testimony', related_name='testimony_reviews', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reply = models.TextField(blank=True, null=True)
    replyed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.full_names + " on " + self.testimony)


class Quote(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='quotes')
    quote = models.TextField()
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.quote[:100]

    def get_absolute_url(self):
        return reverse('quote-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        if self.picture:
            imageTemproary = Image.open(self.picture)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize((450, 450))
            try:
                imageTemproaryResized.save(outputIoStream,
                                           format='JPEG',
                                           quality=150)
            except:
                imageTemproaryResized.save(outputIoStream,
                                           format='PNG',
                                           quality=150)
                try:
                    imageTemproaryResized.save(outputIoStream,
                                               format='GIF',
                                               quality=150)
                except:
                    imageTemproaryResized.save(outputIoStream,
                                               format='BMP',
                                               quality=150)
            outputIoStream.seek(0)
            self.picture = InMemoryUploadedFile(
                outputIoStream, 'ImageField',
                "%s.jpg" % self.picture.name.split('.')[0], 'picture/jpeg',
                sys.getsizeof(outputIoStream), None)
            super(Quote, self).save(*args, **kwargs)
        else:
            self.picture = None
            super(Quote, self).save(*args, **kwargs)


class Devotional(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    bible_reading = models.CharField(max_length=200, blank=True, null=True)
    memory_verse = models.CharField(max_length=200, blank=True, null=True)
    devotion = HTMLField()
    caption_picture = models.ImageField(
        upload_to='devotion', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('devotional-detail', kwargs={'slug': self.slug})

    @property
    def get_reviews(self):
        return self.devotional_reviews.all().order_by('-created_at')

    @property
    def total_reviews(self):
        return DevotionalReview.objects.filter(devotional=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(devotional=self).count()

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(str(self.title))
        if self.caption_picture:
            imageTemproary = Image.open(self.caption_picture)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize((400, 800))
            try:
                imageTemproaryResized.save(outputIoStream,
                                           format='JPEG',
                                           quality=150)
            except:
                imageTemproaryResized.save(outputIoStream,
                                           format='PNG',
                                           quality=150)
                try:
                    imageTemproaryResized.save(outputIoStream,
                                               format='GIF',
                                               quality=150)
                except:
                    imageTemproaryResized.save(outputIoStream,
                                               format='BMP',
                                               quality=150)
                    outputIoStream.seek(0)
                    self.caption_picture = InMemoryUploadedFile(
                        outputIoStream, 'ImageField',
                        "%s.jpg" % self.caption_picture.name.split('.')[0],
                        'caption_picture/jpeg', sys.getsizeof(outputIoStream), None)
            super(Devotional, self).save(*args, **kwargs)
        else:
            self.caption_picture = None
            super(Devotional, self).save(*args, **kwargs)


TYPE = [
    ('course', 'course'),
    ('seminar', 'seminar'),
    ('workshop', 'workshop'),
    ('Ministry', 'Ministry'),
]


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Programme(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    detail = HTMLField()
    prog_image = models.ImageField(upload_to='programme_image')
    programme_category = models.ManyToManyField(Category, blank=True)
    previous_programme = models.ForeignKey('self',
                                           related_name='previous',
                                           on_delete=models.SET_NULL,
                                           blank=True,
                                           null=True)
    next_programme = models.ForeignKey('self',
                                       related_name='next',
                                       on_delete=models.SET_NULL,
                                       blank=True,
                                       null=True)
    publish = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('programme-detail', kwargs={'slug': self.slug})

    @property
    def get_reviews(self):
        return self.programme_reviews.all().order_by('-created_at')

    @property
    def total_reviews(self):
        return ProgrammeReview.objects.filter(programme=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(programme=self).count()

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title))
        if self.prog_image:
            imageTemproary = Image.open(self.prog_image)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize((400, 300))
            try:
                imageTemproaryResized.save(
                    outputIoStream, format='JPEG', quality=150)
            except:
                imageTemproaryResized.save(
                    outputIoStream, format='PNG', quality=150)
                try:
                    imageTemproaryResized.save(
                        outputIoStream, format='GIF', quality=150)
                except:
                    imageTemproaryResized.save(
                        outputIoStream, format='BMP', quality=150)
            outputIoStream.seek(0)
            self.prog_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % self.prog_image.name.split('.')[
                0], 'prog_image/jpeg', sys.getsizeof(outputIoStream), None)
            super(Programme, self).save(*args, **kwargs)
        else:
            self.prog_image = None
            super(Programme, self).save(*args, **kwargs)


class Contact(models.Model):
    full_names = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(
        help_text='subject', max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)


class Testimony(models.Model):
    full_names = models.CharField(max_length=200)
    phone_number = models.CharField(help_text='phone number', max_length=20)
    email = models.EmailField(blank=True, null=True)
    your_testimony = models.TextField()
    add_a_photo = models.ImageField(
        upload_to='Testimony_image', blank=True, null=True)
    previous_testimony = models.ForeignKey('self',
                                           related_name='previous',
                                           on_delete=models.SET_NULL,
                                           blank=True,
                                           null=True)
    next_testimony = models.ForeignKey('self',
                                       related_name='next',
                                       on_delete=models.SET_NULL,
                                       blank=True,
                                       null=True)
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.full_names

    def get_absolute_url(self):
        return reverse('testimony-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.add_a_photo:
            imageTemproary = Image.open(self.add_a_photo)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize((400, 400))
            try:
                imageTemproaryResized.save(outputIoStream,
                                           format='JPEG',
                                           quality=150)
            except:
                imageTemproaryResized.save(outputIoStream,
                                           format='PNG',
                                           quality=150)
                try:
                    imageTemproaryResized.save(outputIoStream,
                                               format='GIF',
                                               quality=150)
                except:
                    imageTemproaryResized.save(outputIoStream,
                                               format='BMP',
                                               quality=150)
            outputIoStream.seek(0)
            self.add_a_photo = InMemoryUploadedFile(
                outputIoStream, 'ImageField',
                "%s.jpg" % self.add_a_photo.name.split('.')[0],
                'add_a_photo/jpeg', sys.getsizeof(outputIoStream), None)
            super(Testimony, self).save(*args, **kwargs)
        else:
            self.add_a_photo = None
            super(Testimony, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_names = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'slug': self.full_names})

    def __str__(self):
        return self.full_names

    def save(self, *args, **kwargs):
        if self.profile_photo:
            imageTemproary = Image.open(self.profile_photo)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize((200, 200))
            try:
                imageTemproaryResized.save(outputIoStream,
                                           format='JPEG',
                                           quality=150)
            except:
                imageTemproaryResized.save(outputIoStream,
                                           format='PNG',
                                           quality=150)
                try:
                    imageTemproaryResized.save(outputIoStream,
                                               format='GIF',
                                               quality=150)
                except:
                    imageTemproaryResized.save(outputIoStream,
                                               format='BMP',
                                               quality=150)
            outputIoStream.seek(0)
            self.profile_photo = InMemoryUploadedFile(
                outputIoStream, 'ImageField',
                "%s.jpg" % self.profile_photo.name.split('.')[0],
                'profile_photo/jpeg', sys.getsizeof(outputIoStream), None)
            super(Profile, self).save(*args, **kwargs)
        else:
            self.profile_photo = None
            super(Profile, self).save(*args, **kwargs)


class Newsletter(models.Model):
    sub_email = models.EmailField(blank=True, null=True)
    subscribe = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_email


class PageWordTags(models.Model):
    devotion_slide = models.TextField(blank=True, null=True)
    prayer_slide = models.TextField(blank=True, null=True)
    quote_slide = models.TextField(blank=True, null=True)
    training_slide = models.TextField(blank=True, null=True)
    any_other_slide_words1 = models.TextField(blank=True, null=True)
    any_other_slide_words2 = models.TextField(blank=True, null=True)

    about_us_intro = models.TextField(blank=True, null=True)
    our_vision = models.TextField(blank=True, null=True)
    our_mission = models.TextField(blank=True, null=True)
    our_message = models.TextField(blank=True, null=True)
    # our_vision = models.TextField(blank=True, null=True)

    special_quotes_intro = models.TextField(blank=True, null=True)
    programme_intro = models.TextField(blank=True, null=True)
    testimony_intro = models.TextField(blank=True, null=True)
    contact_intro = models.TextField(blank=True, null=True)
    contact_address = models.TextField(blank=True, null=True)
    our_social_network_into = models.TextField(blank=True, null=True)
    rhema_word_for_today = models.TextField(blank=True, null=True)


class RhemaWordForToday(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    memory_verse = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.memory_verse
