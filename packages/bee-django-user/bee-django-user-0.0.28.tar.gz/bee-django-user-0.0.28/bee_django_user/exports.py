#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

import datetime
from .models import User, UserLeaveStatus,LOCAL_TIMEZONE


# 获取一个助教，所教的所有学生
def get_teach_users(assistant):
    users = User.objects.filter(userprofile__user_class__assistant=assistant)
    return users


# 获取一个学生是否请假的状态
def get_user_leave_status(user):
    record_list = UserLeaveStatus.objects.filter(user=user, status=1)
    if record_list.exists():
        return 1
    else:
        return 0


# 更新所有请假学生的状态
def update_user_leave_status():
    record_list = UserLeaveStatus.objects.filter(status__in=[1, 2])  # 未处理或请假中
    now = datetime.datetime.now(LOCAL_TIMEZONE)
    for record in record_list:
        # 请假中的学生
        if record.status == 1:
            if record.leave_end >= now:
                record.status = 3
                record.save()
        # 请假中的学生
        elif record.status == 2:
            if record.leave_start >= now:
                record.status = 1
                record.save()
