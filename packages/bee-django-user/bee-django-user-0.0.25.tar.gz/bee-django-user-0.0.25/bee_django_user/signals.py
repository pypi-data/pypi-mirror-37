__author__ = 'bee'
# -*- coding:utf-8 -*-
from django.dispatch import Signal

# 费用审核后的信号
update_user_expire = Signal(providing_args=["leave_record"])