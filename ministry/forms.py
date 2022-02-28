from django import forms
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
    Newsletter
)


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class TestimonyForm(forms.ModelForm):

    class Meta:
        model = Testimony
        fields = ('full_names',
                  'phone_number',
                  'email',
                  'your_testimony',
                  'add_a_photo',
                  )


class DevotionalReviewForm(forms.ModelForm):
    content = forms.CharField(label="Comment", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Type your comment',
            'rows': '4',
            'border': '2px solid #750a20'
        }))

    class Meta:
        model = DevotionalReview
        fields = (
            'full_names',
            'phone_number',
            'email',
            'content',
        )


class DevotionalReviewReplyForm(forms.ModelForm):
    reply = forms.CharField(label="", widget=forms.Textarea(
                                  attrs={
                                      'class': "h6",
                                      'style': 'border-radius: .7em; border: 1px solid #14b3fde3; hover:#14b3fde3;',
                                      'placeholder': 'reply',
                                      'rows': '3',
                                      'cols': '80',
                                  }))

    class Meta:
        model = DevotionalReview
        fields = (
            'reply',
        )


class ProgrammeReviewForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Type your comment',
            'rows': '4',
            'border': '2px solid #750a20'
        }))

    class Meta:
        model = ProgrammeReview
        fields = (
            'full_names',
            'phone_number',
            'email',
            'content',
        )


class ProgrammeReviewReplyForm(forms.ModelForm):
    reply = forms.CharField(label="", widget=forms.Textarea(
                                  attrs={
                                      'class': "h6",
                                      'style': 'border-radius: .7em; border: 1px solid #14b3fde3; hover:#14b3fde3;',
                                      'placeholder': 'reply',
                                      'rows': '3',
                                      'cols': '80',
                                  }))

    class Meta:
        model = ProgrammeReview
        fields = (
            'reply',
        )


class TestimonyReviewForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Type your comment',
            'rows': '4',
            'border': '2px solid #750a20'
        }))

    class Meta:
        model = TestimonyReview
        fields = (
            'full_names',
            'phone_number',
            'email',
            'content',
        )


class TestimonyReviewReplyForm(forms.ModelForm):
    reply = forms.CharField(label="", widget=forms.Textarea(
                                  attrs={
                                      'class': "h6",
                                      'style': 'border-radius: .7em; border: 1px solid #14b3fde3; hover:#14b3fde3;',
                                      'placeholder': 'reply',
                                      'rows': '3',
                                      'cols': '80',
                                  }))

    class Meta:
        model = TestimonyReview
        fields = (
            'reply',
        )
