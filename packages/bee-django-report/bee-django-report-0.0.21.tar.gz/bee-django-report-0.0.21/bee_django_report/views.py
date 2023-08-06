# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, F, Sum, Count
from django.db.models import Case, When, Value, CharField
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from dss.Serializer import serializer
from django.apps import apps
from django.db import connection
from django.contrib import messages

from .utils import get_datetime_with_scope_offset, export_csv, get_user_name
from .dt import get_year_month_week
from .models import ClassWeek, MentorScoreWeek
from .exports import ClassWeekReport, get_section_name, get_class_name
from .forms import MentorScoreWeekForm

User = get_user_model()


# from django.
# Create your views here.
def test(request):
    MentorScoreWeek.update_rank(2018, 26)
    return render(request, 'bee_django_report/report/pie.html', {"title": "统计模版", "subtext": '模拟数据', "data_list": []})


class IndexView(TemplateView):
    template_name = 'bee_django_report/index.html'


class UserGenderView(TemplateView):
    template_name = 'bee_django_report/report/pie.html'
    user_app = 'bee_django_user'
    user_model = 'UserProfile'
    gender_field = 'preuser__gender'
    condition_list = None  # 格式：[{"key": "name", "value": "bee"}]
    gender_list = ((0, "无"), (1, "女"), (2, "男"))
    case_list = [When(preuser__gender=item[0], then=Value(item[1])) for i, item in enumerate(gender_list)]

    def get_context_data(self, **kwargs):
        context = super(UserGenderView, self).get_context_data(**kwargs)
        context["title"] = '学员性别'
        context["subtext"] = ''
        context["data_list"] = self.get_date_list()

        return context

    def get_date_list(self):

        app = apps.get_app_config(self.user_app)
        model = app.get_model(self.user_model)
        kwargs = {}  # 动态查询的字段
        if self.condition_list:
            for i, value in enumerate(self.condition_list):
                kwargs[value["key"]] = value["value"]
        queryset = model.objects.filter(**kwargs).values(self.gender_field).order_by(self.gender_field) \
            .annotate(value=Count(1)) \
            .annotate(name=Case(*self.case_list, default=Value('未填写'), output_field=CharField()))

        return serializer(queryset, output_type='json')


class UserAgeView(TemplateView):
    template_name = 'bee_django_report/report/pie.html'

    def get_sql_str(self):
        sql = '''
        SELECT COUNT(C.age_group), C.age_group FROM
        (SELECT
          CASE
            WHEN B.age >= 50 THEN '50以上'
            WHEN B.age >= 40 THEN '40-50'
            WHEN B.age >= 30 THEN '30-40'
            WHEN B.age >= 20 THEN '20-30'
            WHEN B.age < 20 THEN '20以下'
            ELSE '无'
          END AS age_group
        FROM
        (SELECT (A.this_year - A.birth_year) AS age
        FROM
        (SELECT EXTRACT(YEAR FROM CURRENT_DATE) AS this_year, EXTRACT(YEAR FROM "bee_django_crm_preuser".birthday) AS birth_year
        FROM "bee_django_user_profile" INNER JOIN "bee_django_crm_preuser" ON "bee_django_user_profile".preuser_id = "bee_django_crm_preuser".id) AS A) AS B ) AS C GROUP BY C.age_group
        '''

        return sql

    def get_context_data(self, **kwargs):
        context = super(UserAgeView, self).get_context_data(**kwargs)
        context["title"] = '学员年龄'
        context["subtext"] = ''
        context["data_list"] = self.get_date_list()

        return context

    def get_date_list(self):
        with connection.cursor() as cursor:
            cursor.execute(self.get_sql_str())
            data = cursor.fetchall()
        rc = []
        for i in data:
            rc.append({"name": i[1], "value": i[0]})
        return json.dumps(rc)

        # return [
        #     {"name": 'A1', "value": 12121},
        #     {"name": 'B1', "value": 23231},
        #     {"name": 'C1', "value": 19191}
        # ]


class ClassWeekView(TemplateView):
    template_name = 'bee_django_report/report/class/week.html'

    def get_offset(self):
        offset = self.request.GET.get("offset")
        if not offset:
            offset = -1
        return int(offset)

    def check_save(self):
        class_id = self.kwargs["class_id"]
        ClassWeekReport().auto_save_db(class_id=class_id, offset=self.get_offset())

    def get_data(self):
        self.check_save()
        class_id = self.kwargs["class_id"]
        offset = self.get_offset()
        start_dt, end_dt = get_datetime_with_scope_offset("week", offset)
        year, month, week = get_year_month_week(start_dt)
        records = ClassWeek.objects.filter(class_id=class_id, year=year, week=week)
        return records, class_id, year, week, start_dt, end_dt, offset

    def get_context_data(self, **kwargs):
        context = super(ClassWeekView, self).get_context_data(**kwargs)
        records, class_id, year, week, start_dt, end_dt, offset = self.get_data()
        context["records"] = records
        context["class_id"] = class_id
        context["year"] = year
        context["week"] = week
        context["start_dt"] = start_dt
        context["end_dt"] = end_dt
        context["prev_week"] = offset - 1
        if offset < -1:
            context["next_week"] = offset + 1
        return context

    def get_export_user_name(self, record):
        if record.type_int == 1:
            return '共计'
        if record.type_int == 2:
            return '平均'
        if record.type_int == 3:
            return get_user_name(record.user)
        if record.type_int == 9:
            return '助教：' + get_user_name(record.mentor)

    def get(self, request, *args, **kwargs):
        if request.GET.get("export"):
            records, class_id, year, week, start_dt, end_dt, offset = self.get_data()
            rows = ([
                        (i + 1).__str__(),
                        self.get_export_user_name(record).encode('utf-8'),
                        get_section_name(record.last_user_section_id).encode('utf-8'),
                        record.live_mins,
                        record.live_days,
                        record.live_count,
                        record.feed_count,

                    ] for i, record in enumerate(records))
            headers = [
                '序号'.encode('utf-8'),
                '姓名'.encode('utf-8'),
                '进度'.encode('utf-8'),
                '练习分钟'.encode('utf-8'),
                '练习天数'.encode('utf-8'),
                '练习次数'.encode('utf-8'),
                '日志数'.encode('utf-8'),
            ]
            class_name = get_class_name(class_id)
            csv_name = "[" + class_name + "]" + year.__str__() + "年第" + week.__str__() + "周报表"
            return export_csv(csv_name.encode('utf-8'), headers, rows)
        else:
            return super(ClassWeekView, self).get(request, *args, **kwargs)


# ==========助教周评分===========
class MentorScoreList(ListView):
    template_name = 'bee_django_report/mentor_score/list.html'
    context_object_name = 'score_list'
    paginate_by = 20
    queryset = None

    # def get(self, request, *args, **kwargs):
    #     year, week = self.get_year_week()
    #     if year and week:
    #         MentorScoreWeek.update_rank(year, week)
    #         messages.success(self.request, '已更新排名')
    #     return super(MentorScoreList,self).get(request, *args)

    def get_user(self):
        user_id = self.kwargs["user_id"]
        if not user_id in [0, None]:
            try:
                mentor = User.objects.get(id=user_id)
                return mentor
            except:
                pass
        return None

    def get_year_week(self):
        year = self.request.GET.get("year")
        week = self.request.GET.get("week")
        return year, week

    def get_queryset(self):
        queryset = MentorScoreWeek.objects.all()
        mentor = self.get_user()
        if mentor:
            queryset = queryset.filter(mentor=mentor).order_by('-year', 'week')
        year, week = self.get_year_week()
        if year:
            queryset = queryset.filter(year=year)
        if week:
            queryset = queryset.filter(week=week).order_by('-score')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MentorScoreList, self).get_context_data(**kwargs)
        mentor = self.get_user()
        year, week = self.get_year_week()
        if mentor:
            context["mentor"] = mentor
        if year:
            context["year"] = year
        if week:
            context["week"] = week
        return context


class MentorScoreCreate(CreateView):
    model = MentorScoreWeek
    form_class = MentorScoreWeekForm
    template_name = 'bee_django_report/mentor_score/form.html'

    def get_success_url(self):
        return reverse_lazy('bee_django_report:mentor_score_list', kwargs=self.kwargs)

    def form_valid(self, form):
        # form.instance.mentor_id = self.kwargs["user_id"]
        record = form.save(commit=False)
        record.mentor_id = self.kwargs["user_id"]
        record.save()
        MentorScoreWeek.update_rank(record.year, record.week)
        # return super(MentorScoreCreate, self).form_valid(form)
        return redirect(reverse_lazy('bee_django_report:mentor_score_list', kwargs=self.kwargs))


class MentorScoreUpdate(UpdateView):
    model = MentorScoreWeek
    form_class = MentorScoreWeekForm
    template_name = 'bee_django_report/mentor_score/form.html'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        try:
            old = MentorScoreWeek.objects.get(id=pk)
        except:
            old = None
        record = form.save(commit=True)
        if old:
            MentorScoreWeek.update_rank(old.year, old.week)
        MentorScoreWeek.update_rank(record.year, record.week)
        return redirect(reverse_lazy('bee_django_report:mentor_score_list', kwargs={"user_id": 0}))

        # def get_context_data(self, **kwargs):
        #     context = super(MentorScoreUpdate, self).get_context_data(**kwargs)
        #     context["source"] = Source.objects.get(id=self.kwargs["pk"])
        #     return context


class MentorScoreDelete(DeleteView):
    model = MentorScoreWeek
    success_url = None

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        record = self.get_object()
        record.delete()
        MentorScoreWeek.update_rank(record.year, record.week)
        return redirect(reverse_lazy('bee_django_report:mentor_score_list', kwargs={"user_id": 0}))


# 班级学习进度
class UserClassProgress(TemplateView):
    template_name = "bee_django_report/report/class/progress.html"

    def get_users(self):
        try:
            from bee_django_user.models import UserClass
            class_id = self.kwargs["class_id"]
            user_class = UserClass.objects.get(id=class_id)
            return user_class.get_students()

        except:
            return []

    # 获取最后一个学到的课件
    def get_last_section(self, user):
        try:
            from bee_django_course.exports import get_user_last_course_section
            ucs = get_user_last_course_section(user)
            return ucs
        except:
            return None

    def get_context_data(self, **kwargs):
        context = super(UserClassProgress, self).get_context_data(**kwargs)
        users = self.get_users()
        data_list = []
        for user in users:
            data = {}
            data["user"] = user
            ucs = self.get_last_section(user)
            if ucs:
                data["ucs_id"] = ucs.id
                data["section_has_videowork"] = ucs.section.has_videowork
                data["section_video_length_req"] = ucs.section.video_length_req
                data["ucs_work_time"] = ucs.work_time
            data_list.append(data)
        context["data_list"] = data_list
        return context
