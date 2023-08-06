#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

from django.conf.urls import include, url
from . import views

app_name = 'bee_django_track'
urlpatterns = [
    url(r'^test$', views.test, name='test'),
    url(r'^record/list/(?P<user_id>[0-9]+)/$', views.RecordList.as_view(), name='record_list'),
    url(r'^record/detail/(?P<pk>[0-9]+)/$', views.RecordDetail.as_view(), name='record_detail'),
    url(r'^record/add/(?P<user_id>[0-9]+)/$', views.RecordCreate.as_view(), name='record_add'),
    url(r'^record/update/(?P<pk>[0-9]+)/$', views.RecordUpdate.as_view(), name='record_update'),
    url(r'^record/delete/(?P<pk>[0-9]+)/$', views.RecordDelete.as_view(), name='record_delete'),
]
