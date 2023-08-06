#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

from django.conf.urls import include, url
from . import views

app_name = 'bee_django_report'
urlpatterns = [
    url(r'^test$', views.test, name='test'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^user/gender/$', views.UserGenderView.as_view(), name='user_gender'),
    url(r'^user/age/$', views.UserAgeView.as_view(), name='user_age'),
    # 报表
    url(r'^class/week/(?P<class_id>[0-9]+)/$', views.ClassWeekView.as_view(), name='class_week'),
    # 助教评分
    url(r'^mentor/score/list/(?P<user_id>[0-9]+)/$', views.MentorScoreList.as_view(), name='mentor_score_list'),
    url(r'^mentor/score/add/(?P<user_id>[0-9]+)/$', views.MentorScoreCreate.as_view(), name='mentor_score_add'),
    url(r'^mentor/score/update/(?P<pk>[0-9]+)/$', views.MentorScoreUpdate.as_view(), name='mentor_score_update'),
    url(r'^mentor/score/delete/(?P<pk>[0-9]+)/$', views.MentorScoreDelete.as_view(), name='mentor_score_delete'),
    #     班级学习进度
    url('^user_class/progress/(?P<class_id>\d+)/$', views.UserClassProgress.as_view(), name='user_class_progress'),
]
