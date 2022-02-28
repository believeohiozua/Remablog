from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    PostView,
    ProgrammeReview,
    DevotionalReview,
    TestimonyReview,
    Quote,
    Devotional,
    Category,
    Programme,
    Testimony,
    Contact,
    Profile,
    Newsletter,
    PageWordTags,
    RhemaWordForToday
)


def auto_publish_ON(modeladmin, request, queryset):
    queryset.update(publish=True)


def auto_publish_OFF(modeladmin, request, queryset):
    queryset.update(publish=False)


auto_publish_ON.short_description = 'Publish'
auto_publish_OFF.short_description = 'Turn OFF'


admin.site.register(Category)
admin.site.register(ProgrammeReview)
admin.site.register(DevotionalReview)
admin.site.register(TestimonyReview)
admin.site.register(PostView)
admin.site.register(Contact)
admin.site.register(Newsletter)
admin.site.register(PageWordTags)
# admin.site.register()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class ProgrammeReviewInline(admin.StackedInline):
    model = ProgrammeReview
    can_delete = True
    verbose_name_plural = 'ProgrammeReview'


class DevotionalReviewInline(admin.StackedInline):
    model = DevotionalReview
    can_delete = True
    verbose_name_plural = 'DevotionalReview'


class TestimonyReviewInline(admin.StackedInline):
    model = TestimonyReview
    can_delete = True
    verbose_name_plural = 'TestimonyReview'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


@admin.register(Programme)
class Programme(admin.ModelAdmin):
    list_display = ('title', 'publish',
                    'previous_programme', 'next_programme')
    list_filter = ('programme_category',)
    actions = [auto_publish_ON, auto_publish_OFF]
    # inlines = (ProgrammeReviewInline, )


@admin.register(Devotional)
class Devotional(admin.ModelAdmin):
    list_display = ('title', 'date', 'publish',)
    actions = [auto_publish_ON, auto_publish_OFF]
    # inlines = (DevotionalReviewInline, )


@admin.register(Testimony)
class Testimony(admin.ModelAdmin):
    list_display = ('full_names',  'publish',
                    'previous_testimony', 'next_testimony',)
    actions = [auto_publish_ON, auto_publish_OFF]
    # inlines = (TestimonyReviewInline, )


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('full_names',)


@admin.register(Quote)
class Quote(admin.ModelAdmin):
    list_display = ('quote', 'publish',)
    actions = [auto_publish_ON, auto_publish_OFF]


@admin.register(RhemaWordForToday)
class RhemaWordForToday(admin.ModelAdmin):
    list_display = ('memory_verse', 'publish',)
    actions = [auto_publish_ON, auto_publish_OFF]
