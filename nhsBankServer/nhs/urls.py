from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import AllUserData


class HomePageView(TemplateView):
    template_name = 'index.html'


urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view()),
    url(r'^devices/', include('devices.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^channels/', include('channels.urls')),
    url(r'^completedata/$', AllUserData.as_view()),
)
