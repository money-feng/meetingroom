from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

user = get_user_model()

class MeetingRoomEquipment(models.Model):
    """会议室设备"""
    name = models.CharField(max_length=50, verbose_name='设备名称')

    class Meta:
        verbose_name = '会议室设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MeetingRoomInfos(models.Model):
    """会议室信息"""
    ROOM_STATUS = (
        (0, '正常'),
        (1, '报修'),
        (2, '占用'),
        (3, '停用')
    )
    RESERVE_STATUS = (
        (0, '可预订'),
        (1, '已预订')
    )
    name = models.CharField(max_length=20, verbose_name='名称')
    site = models.CharField(max_length=100, verbose_name='会议室位置')
    nums = models.PositiveIntegerField(verbose_name='人数')
    equipment = models.ManyToManyField(MeetingRoomEquipment, verbose_name='设备')
    status = models.PositiveSmallIntegerField(choices=ROOM_STATUS, default=0, verbose_name='状态')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    add_user = models.ForeignKey(user, on_delete=models.DO_NOTHING, verbose_name='添加用户')
    reserve_status = models.PositiveSmallIntegerField(choices=RESERVE_STATUS, default=0, verbose_name='预定状态')
    image = models.ImageField(upload_to='meetingroom', default='liqin.jpg', verbose_name='会议室图片')

    class Meta:
        verbose_name = '会议室信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def equipment_name(self):
        return ', '.join([equipment.name for equipment in self.equipment.all()])

    @property
    def room_status(self):
        return self.get_status_display()

    @property
    def manager(self):
        return self.add_user.name

    @property
    def reserve(self):
        return self.get_reserve_status_display()