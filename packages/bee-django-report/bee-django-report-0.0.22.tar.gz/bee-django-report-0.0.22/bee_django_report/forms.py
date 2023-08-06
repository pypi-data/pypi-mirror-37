# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms

from .models import MentorScoreWeek

class MentorScoreWeekForm(forms.ModelForm):
    class Meta:
        model = MentorScoreWeek
        fields = ['year', "week", "score", "info"]

    # def update_rank(self):
