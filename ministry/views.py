from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.views import generic
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from io import BytesIO
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import base64
from django.core.files.base import ContentFile
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
from .forms import (
    ContactForm,
    DevotionalReviewForm,
    DevotionalReviewReplyForm,
    ProgrammeReviewForm,
    ProgrammeReviewReplyForm,
    TestimonyReviewForm,
    TestimonyReviewReplyForm,
    TestimonyForm,
)


def pageTage():
    return PageWordTags.objects.get(pk=1)

# convert base64 to png and save to database


def base64Converter(input):
    format, imgstr = str(input).split(';base64,')
    ext = format.split('/')[-1]
    processed_img = ContentFile(base64.b64decode(
        imgstr), name=str('testimony' + ext))
    return processed_img


def testing(request):
    context = {'title_tag': 'RHEMATOSE: TEST PAGE'}
    return render(request, 'test.html', context)


def newsletter(arg):
    if arg.request.POST.get("sub_email"):
        newsletter, created = Newsletter.objects.get_or_create(
            sub_email=arg.request.POST.get("sub_email"),
            subscribe=True
        )
        newsletter.save()
        return messages.info(arg.request, "SUBSCRIBED!")


class IndexView(generic.View):
    def post(self, request, *args, **kwargs):
        newsletter(self)

        if request.POST.get("full_names") and request.POST.get("email") and request.POST.get("subject") and request.POST.get("message"):
            contact, created = Contact.objects.get_or_create(
                full_names=request.POST.get("full_names"),
                email=request.POST.get("email"),
                message=request.POST.get("message")
            )
            contact.save()

            subject = str("Contact:  " + request.POST.get("subject") +
                          " from " + request.POST.get("full_names"))
            message = '%s' % (request.POST.get("message"))
            emailFrom = request.POST.get("email")
            emailTo = ['rhematose@hotmail.com']
            send_mail(subject, message, emailFrom, emailTo,
                      fail_silently=True),
            messages.info(request,
                          "Thanks reaching-out to us. God Bless you.")
        if request.is_ajax():
            context = {'contact': True}
            html = render_to_string(
                'search_section.html', context, request=request)
            return JsonResponse({'form': html})

        # if request.POST.get("sub_email"):
        #     newsletter, created = Newsletter.objects.get_or_create(
        #         sub_email=request.POST.get("sub_email"),
        #         subscribe=True
        #     )
        #     newsletter.save()

    def get(self, request, *args, **kwargs):
        seminars_counter = Programme.objects.filter(
            programme_category__category__contains='seminar').count()
        quotes_counter = Quote.objects.all().count()
        workshops_counter = Programme.objects.filter(
            programme_category__category__contains='workshop').count()
        courses_counter = Programme.objects.filter(
            programme_category__category__contains='course').count()
        devotional_of_the_day = Devotional.objects.filter(
            publish=True).order_by('-created_at')[:1]
        special_quotes = Quote.objects.filter(
            publish=True).order_by('-created_at')[:6]
        programmes = Programme.objects.filter(
            publish=True).order_by('-created_at')[:9]
        testimonies = Testimony.objects.filter(
            publish=True).order_by('-created_at')
        context = {'title_tag': 'RHEMATOSE: HOME',
                   'seminars_counter': seminars_counter,
                   'quotes_counter': quotes_counter,
                   'workshops_counter': workshops_counter,
                   'courses_counter': courses_counter,
                   'devotional_of_the_day': devotional_of_the_day,
                   'special_quotes': special_quotes,
                   'programmes': programmes,
                   'testimonies': testimonies,
                   'Pagetag': pageTage(),
                   'RhemaWordForToday': RhemaWordForToday.objects.filter(publish=True).order_by('-created_at')[:1],

                   }
        return render(request, 'index.html', context)


class DevotionalListView(generic.ListView):
    model = Devotional
    paginate_by = 4
    template_name = 'components/devotional_list.html'

    def get_queryset(self):
        return Devotional.objects.filter(publish=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tag'] = 'RHEMATOSE: DEVOTIONAL'
        context['Pagetag'] = PageWordTags.objects.get(pk=1)
        return context


class DevotionalDetailView(generic.DetailView):
    model = Devotional
    context_object_name = 'devotional'
    template_name = 'components/devotional_detail.html'
    form = DevotionalReviewForm()

    def get_object(self):
        obj = super().get_object()
        PostView.objects.get_or_create(devotional=obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tag'] = 'RHEMATOSE: DEVOTIONAL'
        context['Pagetag'] = PageWordTags.objects.get(pk=1)
        context['form'] = self.form
        context['devotionalreviewreplyForm'] = DevotionalReviewReplyForm
        return context

    def post(self, request, *args, **kwargs):
        devotional = self.get_object()
        form = DevotionalReviewForm(request.POST)
        reply = DevotionalReviewReplyForm(request.POST)
        if form.is_valid():
            form.instance.devotional = devotional
            form.save()
            messages.info(request,
                          "Thank you Comment, God Bless you.")
            if request.is_ajax():
                context = {
                    'full_names': form.instance.full_names,
                    'content': form.instance.content
                }
                html = render_to_string(
                    'components/reviews.html', context, request=request)
                return JsonResponse({'form': html})
            else:
                return redirect(reverse("devotional-detail", kwargs={'slug': devotional.slug}))
        if reply.is_valid():
            target_review = request.POST.get('target_review')
            add_reply = DevotionalReview.objects.get(pk=target_review)
            add_reply.user = request.user
            add_reply.reply = request.POST.get('reply')
            add_reply.replyed = True
            add_reply.save()
            messages.info(request,
                          "You Have Replied")
            if request.is_ajax():
                html = render_to_string(
                    'components/reviews.html', request=request)
                return JsonResponse({'form': html})
            else:
                return redirect(reverse("devotional-detail", kwargs={'slug': devotional.slug}))


class ProgrammeListView(generic.ListView):
    model = Programme
    paginate_by = 4
    template_name = 'components/programme_list.html'

    def get_queryset(self):
        return Programme.objects.filter(publish=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tag'] = 'RHEMATOSE: PROGRAMME'
        context['Pagetag'] = PageWordTags.objects.get(pk=1)
        return context


class ProgrammeDetailView(generic.DetailView):
    model = Programme
    context_object_name = 'programme'
    template_name = 'components/programme_detail.html'
    form = ProgrammeReviewForm()

    def get_object(self):
        obj = super().get_object()
        PostView.objects.get_or_create(programme=obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tag'] = 'RHEMATOSE: PROGRAMMES'
        context['Pagetag'] = PageWordTags.objects.get(pk=1)
        context['form'] = self.form
        context['programmereviewreplyForm'] = ProgrammeReviewReplyForm
        return context

    def post(self, request, *args, **kwargs):
        programme = self.get_object()
        form = ProgrammeReviewForm(request.POST)
        reply = ProgrammeReviewReplyForm(request.POST)
        if form.is_valid():
            form.instance.programme = programme
            form.save()
            messages.info(request,
                          "Thank you Comment, God Bless you.")
        if reply.is_valid():
            target_review = request.POST.get('target_review')
            add_reply = ProgrammeReview.objects.get(pk=target_review)
            add_reply.user = request.user
            add_reply.reply = request.POST.get('reply')
            add_reply.replyed = True
            add_reply.save()
            messages.info(request,
                          "You Have Replied")
        return redirect(reverse("programme-detail", kwargs={'slug': programme.slug}))


class TestimonyListView(generic.ListView):
    model = Testimony
    paginate_by = 4
    template_name = 'components/testimony_list.html'

    def get_queryset(self):
        return Testimony.objects.filter(publish=True).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        testimony_form = TestimonyForm(
            request.POST, request.FILES)
        if testimony_form.is_valid():
            testimony_form.instance.add_a_photo = base64Converter(
                request.POST.get('add_a_photo'))
            testimony_form.save()
        if request.is_ajax():
            context = {'testimony': True}
            html = render_to_string(
                'search_section.html', context, request=request)
            return JsonResponse({'form': html})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tag'] = 'RHEMATOSE: TESTIMONY'
        context['Pagetag'] = PageWordTags.objects.get(pk=1)
        context['testimony_form'] = TestimonyForm()
        return context


class TestimonyDetailView(generic.DetailView):
    model = Testimony
    context_object_name = 'testimony'
    template_name = 'components/testimony_detail.html'
    form = TestimonyReviewForm()

    def get_object(self):
        obj = super().get_object()
        PostView.objects.get_or_create(testimony=obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tag'] = 'RHEMATOSE: TESTIMONY'
        context['Pagetag'] = PageWordTags.objects.get(pk=1)
        context['form'] = self.form
        context['testimonyreviewreplyForm'] = TestimonyReviewReplyForm
        return context

    def post(self, request, *args, **kwargs):
        testimony = self.get_object()
        form = TestimonyReviewForm(request.POST)
        reply = TestimonyReviewReplyForm(request.POST)
        if form.is_valid():
            form.instance.testimony = testimony
            form.save()
            messages.info(request,
                          "Thank you Comment, God Bless you.")
        if reply.is_valid():
            target_review = request.POST.get('target_review')
            add_reply = TestimonyReview.objects.get(pk=target_review)
            add_reply.user = request.user
            add_reply.reply = request.POST.get('reply')
            add_reply.replyed = True
            add_reply.save()
            messages.info(request,
                          "You Have Replied")
        return redirect(reverse("testimony-detail", kwargs={'slug': testimony.slug}))


class QuoteDetailView(generic.DetailView):
    model = Quote
    context_object_name = 'quote'
    template_name = 'components/quote_detail.html'


class QuoteListView(generic.ListView):
    model = Quote
    paginate_by = 8
    template_name = 'components/quote_list.html'

    def get_queryset(self):
        return Quote.objects.filter(publish=True).order_by('-created_at')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title_tag'] = 'RHEMATOSE: QUOTES'
        context['Pagetag'] = pageTage()
        return context


def Search(request):
    context = {'title_tag': 'RHEMATOSE: SEARCH PAGE'}
    opt = request.POST.get("opt")
    search = request.POST.get("search")
    if search and opt:
        if opt == 'devotion':
            search_result = Devotional.objects.all().filter(
                Q(devotion__icontains=search)
                | Q(title__icontains=search)
                | Q(bible_reading__icontains=search)
                | Q(date__icontains=search)
            ).distinct()
            context.update({
                'search_result': search_result,
                'done': True
            })
        elif opt == 'quotes':
            search_result = Quote.objects.all().filter(
                Q(quote__icontains=search)
            ).distinct()
            context.update({
                'search_result': search_result,
                'done': True
            })
        elif opt == 'testimonies':
            search_result = Testimony.objects.all().filter(
                Q(full_names__icontains=search)
                | Q(phone_number__icontains=search)
                | Q(email__icontains=search)
                | Q(your_testimony__icontains=search)
            ).distinct()
            context.update({
                'search_result': search_result,
                'done': True
            })
        elif opt == 'course' or opt == 'seminar' or opt == 'workshop':
            search_result = Programme.objects.all().filter(
                Q(title__icontains=search)
                | Q(detail__icontains=search)
                | Q(programme_category__category__icontains=search)
            ).distinct()
            context.update({
                'search_result': search_result,
                'done': True
            })

    if request.is_ajax():
        html = render_to_string('search_section.html',
                                context,
                                request=request)
        return JsonResponse({'form': html})
    else:
        return render(request, 'Search.html', context)
