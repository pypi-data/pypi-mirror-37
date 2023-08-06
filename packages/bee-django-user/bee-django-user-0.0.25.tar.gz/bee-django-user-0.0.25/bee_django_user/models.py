# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime, pytz
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.apps import apps
from django.conf import settings
from bee_django_crm.models import PreUser
from .signals import update_user_expire as update_user_expire_signal

LOCAL_TIMEZONE = pytz.timezone('Asia/Shanghai')


# Create your models here.


# def get_crm_preuser():
#     if settings.CRM_PREUSER:
#         return settings.CRM_PREUSER
#     return None


# 用户，扩展的user
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    student_id = models.IntegerField(verbose_name='学号', unique=True, null=True)
    room_id = models.CharField(max_length=180, verbose_name='习琴室ID', null=True, blank=True)
    user_class = models.ForeignKey('bee_django_user.UserClass', verbose_name='用户班级', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='开课日期')
    expire_date = models.DateTimeField(null=True, blank=True, verbose_name='结课日期')
    preuser = models.OneToOneField(settings.CRM_PREUSER, verbose_name='crm用户', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bee_django_user_profile'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('can_manage', '可以访问后台管理'),
            ('can_change_user_group', '可以修改用户组'),
            ('reset_user_password', '可以重置用户密码'),
            ('view_all_users', '可以查看所有用户'),
            ('view_manage_users', '可以查看管理的用户'),
            ('view_teach_users', '可以查看教的用户'),
        )

    def __str__(self):
        return self.user.username

    def has_group(self, group_name):
        group_name_list = []
        for group in self.user.groups.all():
            group_name_list.append(group.name)
        print(group_name_list)
        if group_name in group_name_list:
            return True
        return False

    @classmethod
    def fix_cc_room_id(cls):
        try:
            from bee_django_course.cc import create_room
            for e in cls.objects.all():
                if not e.room_id:
                    room_id = create_room(e.preuser.name + '的直播间')
                    if room_id:
                        e.room_id = room_id
                        e.save()
        except:
            return

            # def has_manage(self):
            #     try:
            #         if self.has_group("管理员") or self.has_group("客服") or self.has_group("助教"):
            #             return True
            #     except:
            #         return False
            #     return False

            # # 获取学生列表数据集
            # def get_user_list_queryset(self):
            #     if self.has_group("管理员") or self.has_group("客服"):
            #         return User.objects.all()
            #     elif self.has_group("助教"):
            #         return User.objects.filter(userprofile__user_class__assistant__userprofile=self)
            #     return []


@receiver(post_save, sender=UserProfile)
def create_user(sender, **kwargs):
    user_pofile = kwargs['instance']
    if kwargs['created']:
        user = User.objects.create_user(username=settings.USER_EX_USERNAME + user_pofile.student_id.__str__(),
                                        password=settings.USER_DEFAULT_PASSWORD)
        user.first_name = user_pofile.preuser.name
        user.save()
        user_pofile.user = user
        user_pofile.save()
        try:
            group = Group.objects.get(name='学生')
            user.groups.add(group)
        except Exception as e:
            print(e)



            # user_profile_list = UserProfile.objects.all().order_by("-student_id")
            # if user_profile_list.count() >= 1:
            #     max_student_id = user_profile_list.first().student_id
            # else:
            #     max_student_id = 0

    return


# @receiver(post_save, sender=User)
# def create_user_profile(sender, **kwargs):
#     user = kwargs['instance']
#     if kwargs['created']:
#         user_profile_list = UserProfile.objects.all().order_by("-student_id")
#         if user_profile_list.count() >= 1:
#             max_student_id = user_profile_list.first().student_id
#         else:
#             max_student_id = 0
#         user_profile = UserProfile(user=user)
#         user_profile.student_id = max_student_id + 1
#         user_profile.save()
#     return
# 如果有crm，则创建并关联crm用户
# res = apps.is_installed("bee_django_crm")
# if not res:
#     return
# try:
#     from bee_django_crm.models import PreUser
#     preuser = PreUser(user=user)
#     preuser.save()
# except:
#     return

USER_LEAVE_TYPE_CHOICES = ((1, '请假'), (2, "请假有销假"), (3, '延期'), (4, '提前'))


class UserLeaveRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leave_user')
    type = models.IntegerField(choices=USER_LEAVE_TYPE_CHOICES, default=1, verbose_name='类型')
    start = models.DateTimeField(null=True, blank=True, verbose_name='开始日期')
    end = models.DateTimeField(null=True, blank=True, verbose_name='结束日期')
    old_expire = models.DateTimeField(blank=True, verbose_name='原结课日期', null=True)
    new_expire = models.DateTimeField(blank=True, verbose_name='新结课日期')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='create_user')
    created_at = models.DateTimeField(auto_now_add=True)
    is_check = models.BooleanField(default=False, verbose_name='通过审核')
    check_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='check_user')
    check_at = models.DateTimeField(null=True)
    info = models.TextField(verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'bee_django_user_leave_record'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('change_check', '可以审核用户的请假'),
        )

    def __str__(self):
        return self.pk.__str__()

    def get_type(self):
        if not self.type:
            return ""
        for g in USER_LEAVE_TYPE_CHOICES:
            if self.type == g[0]:
                return g[1]
        return ""

    # 审核请假记录后，自动更新用户的结课日期
    def update_user_expire(self):
        if self.ischeck == True:
            user = self.user
            user.userprofile.expire_date = self.new_expire
            user.userprofile.save()
        return


# 学生请假状态表
class UserLeaveStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.IntegerField(default=0)  # 1请假中，2正常-请假期未到，3正常-请假期已处理完成
    leave_start = models.DateTimeField(null=True, blank=True, verbose_name='请假开始日期')
    leave_end = models.DateTimeField(null=True, blank=True, verbose_name='请假结束日期')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    record = models.ForeignKey(UserLeaveRecord, null=True)  #

    class Meta:
        db_table = 'bee_django_user_leave_status'
        app_label = 'bee_django_user'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username + ",status:" + self.status.__str__()

    def update_status(self):
        now = datetime.datetime.now(tz=LOCAL_TIMEZONE)
        # 请假中的学生
        if self.status == 1:
            if (self.leave_end - now).days < 0:
                self.status = 3
                self.save()
        # 新添加的学生，或未到请假期的学生
        elif self.status in [0, 2]:
            if (self.leave_start - now).days <= 0:
                self.status = 1
                self.save()
            if (self.leave_end - now).days < 0:
                self.status = 3
                self.save()
        return

    def get_status(self):
        if self.status == 1:
            return '请假中'
        elif self.status == 2:
            return '请假期未到'
        elif self.status == 3:
            return '请假期已处理完成'

        return ''


# 审核请假记录后
# 1.自动更新用户的结课日期
# 2.自动更新到用户状态表
# 3.发送信号，创建一条足迹
@receiver(post_save, sender=UserLeaveRecord)
def update_user_expire(sender, **kwargs):
    record = kwargs['instance']
    if kwargs['created'] == False and record.is_check == True:
        # 自动更新用户的结课日期
        user = record.user
        user.userprofile.expire_date = record.new_expire
        user.userprofile.save()
        # 发送信号
        update_user_expire_signal.send(sender=UserLeaveRecord, leave_record=record)
        # 请假
        if record.type == 1:
            n = UserLeaveStatus()
            n.user = record.user
            n.leave_start = record.start
            n.leave_end = record.end
            n.record = record
            n.save()
            # 更新状态
            n.update_status()
        # 销假
        elif record.type == 2:
            try:
                n = UserLeaveStatus.objects.get(record=record)
            except:
                return
            n.leave_start = record.start
            n.leave_end = record.end
            n.save()
            # 更新状态
            n.update_status()
    return


# 班级
class UserClass(models.Model):
    name = models.CharField(max_length=180, verbose_name='班级名称')
    assistant = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='助教', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bee_django_user_class'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('view_all_classes', '可以查看所有班级'),
            ('view_manage_classes', '可以查看管理的班级'),
            ('view_teach_classes', '可以查看教的班级'),
        )

    def get_students(self):
        user_profile_list = self.userprofile_set.all()
        user_list = User.objects.filter(userprofile__in=user_profile_list)
        return user_list


def get_user_name(self):
    return self.first_name


# 学生列表页根据student_id搜索
def get_user_search_link(self):
    ex_link = "/user/list/?student_id="
    search = self.userprofile.student_id.__str__()
    return ex_link + search


User.add_to_class("__unicode__", get_user_name)
User.add_to_class("get_user_search_link", get_user_search_link)
