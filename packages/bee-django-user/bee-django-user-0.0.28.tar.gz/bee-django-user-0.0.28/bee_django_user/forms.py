# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms
from django.contrib.auth.models import User, Group

from .models import UserProfile, UserClass, UserLeaveRecord, USER_LEAVE_TYPE_CHOICES
from django.forms.models import inlineformset_factory


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name"]


class UserSearchForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='用户组', required=False)
    student_id = forms.CharField(label='学号', required=False)
    first_name = forms.CharField(label='用户姓名', required=False)


    # class Meta:
    #     model = User
    #     fields = ["student_id","first_name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['start_date', "user_class"]


profile_inline_formset = inlineformset_factory(User, UserProfile, form=UserProfileForm, can_delete=False)


class UserClassForm(forms.ModelForm):
    assistant_queryset = User.objects.filter(groups__name__in=['助教'])
    assistant = forms.ModelChoiceField(queryset=assistant_queryset, label='助教', required=False)

    class Meta:
        model = UserClass
        fields = ["name", 'assistant']


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['groups']


# 请假/延期
class UserLeaveRecordForm(forms.ModelForm):
    type_choices = ((1, "请假"), (3, "延期"))
    type = forms.ChoiceField(choices=type_choices, label='类型')

    class Meta:
        model = UserLeaveRecord
        fields = ['type', "start", "end", "info"]


# 请假/延期
class UserLeaveRecordCancelForm(forms.ModelForm):
    type_choices = ((2, "销假"),)
    type = forms.ChoiceField(choices=type_choices, label='类型')

    class Meta:
        model = UserLeaveRecord
        fields = ['type', "start", "info"]
