__author__ = 'brettlarder'
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = patterns('',
                       url(r'^apns/$', views.APNSDeviceList.as_view()),
                       url(r'^apns/(?P<pk>[0-9]+)$', views.APNSDeviceDetail.as_view()),
                       url(r'^sms/$', views.SMSDeviceList.as_view()),
                       url(r'^sms/(?P<pk>[0-9]+)$', views.SMSDeviceDetail.as_view()),
                       url(r'^gcm/$', views.GCMDeviceList.as_view()),
                       url(r'^gcm/(?P<pk>[0-9]+)$', views.GCMDeviceDetail.as_view()),
                       url(r'^mydevices/$', views.MyDevicesList.as_view())
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
