# -*- coding:utf-8 -*-
__author__ = 'bee'
from django.dispatch import Signal

# 费用审核后的信号
update_user_expire_signal = Signal(providing_args=["leave_record"])