#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

from django.conf.urls import include, url
from . import views
app_name = 'bee_django_message'
urlpatterns = [
    url(r'^test$', views.test, name='test'),
    url(r'^$', views.MessageList.as_view(), name='index'),
    # =======消息类型========
    url(r'^message/list/$', views.MessageList.as_view(), name='message_list'),
    url(r'^message/detail/(?P<pk>[0-9]+)/$', views.MessageDetail.as_view(), name='message_detail'),
    url(r'^message/add/$', views.MessageCreate.as_view(), name='message_add'),
    url(r'^message/update/(?P<pk>[0-9]+)/$', views.MessageUpdate.as_view(), name='message_update'),
    url(r'^message/delete/(?P<pk>[0-9]+)/$', views.MessageDelete.as_view(), name='message_delete'),
    # =======发送记录========
    url(r'^user/record/list/(?P<user_id>[0-9]+)/$', views.UserRecordList.as_view(), name='user_record_list'),
    url(r'^user/record/click/$', views.UserRecordClick.as_view(), name='user_record_click'),
    url(r'^user/record/all/click/$', views.UserRecordAllClick.as_view(), name='user_records_all_click'),


]