from django.urls import path, re_path
from .views import (
    testing,
    IndexView,
    Search,
    DevotionalDetailView,
    ProgrammeDetailView,
    TestimonyDetailView,
    QuoteListView,
    QuoteDetailView,
    DevotionalListView,
    ProgrammeListView,
    TestimonyListView
)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('test/', testing, name='test'),
    path('search/', Search, name='Search'),
]
#  LISTVIEWS
urlpatterns += [
    path('quote/', QuoteListView.as_view(), name='quotes'),
    path('devotional/', DevotionalListView.as_view(), name='devotional'),
    path('programme/', ProgrammeListView.as_view(), name='programme'),
    path('testimony/', TestimonyListView.as_view(), name='testimony'),
]
# DETAILVIEWS
urlpatterns += [
    path('devotional/<slug>/', DevotionalDetailView.as_view(),
         name='devotional-detail'),
    path('programme/<slug>/', ProgrammeDetailView.as_view(),
         name='programme-detail'),
    path('testimony/<pk>/', TestimonyDetailView.as_view(),
         name='testimony-detail'),
    path('quote/<pk>/', QuoteDetailView.as_view(),
         name='quote-detail'),
]
