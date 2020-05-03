from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=20, verbose_name='部门名称')
    department_parent = models.OneToOneField('Department', on_delete=models.CASCADE, related_name='parent',
                                             null=True, blank=True, verbose_name='上级部门')
    department_sequence = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='排序')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['department_sequence']

    def __str__(self):
        return self.department_name

class UserProfile(AbstractUser):
    GENDER = (
        (0, '女'),
        (1, '男')
    )
    name = models.CharField(max_length=25, verbose_name='姓名')
    gender = models.PositiveSmallIntegerField(choices=GENDER, null=True, verbose_name='性别')
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name='department',
                                   null=True, verbose_name='部门')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    phone = models.CharField(max_length=13, verbose_name='手机')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @property
    def department_name(self):
        return self.department.department_name

class MenuList(models.Model):
    """菜单"""
    name = models.CharField(max_length=20, verbose_name='名称')
    path = models.CharField(max_length=20, default='', verbose_name='路由')
    parent = models.ForeignKey('MenuList', on_delete=models.CASCADE,
    related_name='parentlevel', null=True, blank=True, verbose_name='上级菜单')
    style = models.CharField(max_length=20, default='el-icon-menu', verbose_name='样式')

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def children(self):
        return self.parentlevel.all().values('id', 'name', 'path', 'style')