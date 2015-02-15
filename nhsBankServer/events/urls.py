__author__ = 'brettlarder'

from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = patterns('',
                       url(r'^$', views.EventList.as_view()),
                       url(r'^(?P<pk>[0-9]+)/$', views.EventDetail.as_view()),
                       url(r'^locations/$', views.LocationList.as_view()),
                       url(r'^locations/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view()),
                       url(r'^tags/$', views.EventTagList.as_view()),
                       url(r'^tags/(?P<pk>[0-9]+)/$', views.EventTagDetail.as_view()),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)