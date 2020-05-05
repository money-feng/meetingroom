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

class Permission(models.Model):
    """权限列表"""
    name = models.CharField(max_length=20, verbose_name='名称')
    path = models.CharField(max_length=20, default='', blank=True, null=True, verbose_name='路由')
    parent = models.ForeignKey('Permission', on_delete=models.CASCADE,
    related_name='parentlevel', null=True, blank=True, verbose_name='上级菜单')
    style = models.CharField(max_length=20, default='el-icon-menu', verbose_name='样式')
    level = models.PositiveSmallIntegerField(verbose_name='级别')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def children(self):
        from .serializers import PermissionModelSerializer
        serializer_data = PermissionModelSerializer(self.parentlevel.all(), many=True)
        # return self.parentlevel.all().values('id', 'name', 'path', 'style','level')
        return serializer_data.data

class Roles(models.Model):
    role_name = models.CharField(max_length=20, verbose_name="角色名称")
    role_desc = models.CharField(max_length=20, verbose_name='角色描述')
    permissions = models.ManyToManyField('Permission', related_name='perm', verbose_name='权限')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.role_name

    @property
    def role_perms(self):
        from .serializers import PermissionModelSerializer
        # 这里需要将每个实例对应的所有permission取出来序列化，次级别权限必定有个父级别，所以这里只取0级权限
        serializer_perms = PermissionModelSerializer(self.permissions.filter(level=0), many=True)
        return serializer_perms.data