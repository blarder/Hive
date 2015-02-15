from . import views

__author__ = 'brettlarder'
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                       url(r'^$', views.users.UserList.as_view()),
                       url(r'^message/$', views.admin.MessageView.as_view()),
                       url(r'^push/$', views.admin.SendPushNotificationsView.as_view()),
                       url(r'^changepass/$', views.authentication.PasswordChange.as_view()),
                       url(r'^login/$', views.authentication.LogInPage.as_view()),
                       url(r'^validate/$', views.authentication.ValidatePage.as_view()),
                       url(r'^logout/$', views.authentication.LogOutPage.as_view()),
                       url(r'^mydata/$', views.users.MyUserPage.as_view()),
                       url(r'^(?P<pk>[0-9]+)/$', views.users.UserDetail.as_view()),
                       url(r'^adminwarnings/$', views.admin.AdminWarningList.as_view()),
                       url(r'^adminwarnings/(?P<pk>[0-9]+)/$', views.admin.AdminWarningDetail.as_view()),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
