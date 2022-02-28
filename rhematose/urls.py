from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', include('ministry.urls')),
    # path('fdhffdffgfdhg009i7u9ioh;ofd/', include('allauth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('secretsof_the_secretplace_admin/', admin.site.urls),
    # url(r'^secretsof_the_secretplace_auth/$', LoginView.as_view(template_name='auth.html'),
    #     name='secretsof_the_secretplace_auth'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]
