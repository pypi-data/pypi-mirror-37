#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'bee'
import json, pytz,csv
from django.conf import settings
from django.apps import apps
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings
from django.http import StreamingHttpResponse

from .models import ClassWeek
from .dt import get_today, add_months, add_weeks

LOCAL_TIMEZONE = pytz.timezone('Asia/Shanghai')


class JSONResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, dict):
            _json_str = json.dumps(obj)
        else:
            _json_str = obj
        super(JSONResponse, self).__init__(_json_str, content_type="application/json;charset=utf-8")


# 获取开始时间和结束时间
# scope：范围：day/month/week
# offset: 偏移时间，正为延后，负为以前

def get_datetime_with_scope_offset(scope, offset):
    today = get_today()
    start_time = None
    end_time = None
    if scope == 'day':
        days = offset
        start_time = (today + datetime.timedelta(days=days))
        end_time = (start_time + datetime.timedelta(days=1))
    elif scope == 'month':
        first_day = (today + datetime.timedelta(days=-today.day + 1))
        start_time = add_months(first_day, offset)
        end_time = add_months(first_day, offset + 1)
    elif scope == 'week':
        start_time, end_time = add_weeks(offset)
    return start_time, end_time


# 获取自定义user的自定义name
def get_user_name(user):
    try:
        return getattr(user, settings.USER_NAME_FIELD)
    except:
        if user:
            return user.username
        else:
            return None


def save_week_report(class_id, year, week, type_int, start_date, end_date, user=None, mentor=None, live_mins=0,
                     feed_count=0, live_days=0, live_count=0, last_user_section_id=None):
    r = ClassWeek()
    r.user = user
    r.class_id = class_id
    r.year = year
    r.week = week
    r.type_int = type_int  # 1-班级总数记录 2-平均数记录 3-班级学生的记录 -9:班级老师的记录
    r.start_date = start_date
    r.end_date = end_date
    r.mentor = mentor  # 助教
    r.live_mins = live_mins  # 练习时长
    r.feed_count = feed_count  # 发表日志数
    r.live_days = live_days  # 练习天数
    r.live_count = live_count  # 练习次数
    r.last_user_section_id = last_user_section_id  # 最后一个学习的课件
    r.save()
    return


# 导出csv
def export_csv(filename, headers, rows):
    response = StreamingHttpResponse((row for row in csv_itertor(headers, rows)), content_type="text/csv;charset=utf-8")
    response['Content-Disposition'] = 'attachment;filename="' + filename + '.csv"'
    return response


def csv_itertor(headers, rows):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    yield writer.writerow(headers)
    for column in rows:
        yield writer.writerow(column)


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


# 完