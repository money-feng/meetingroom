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
    name = models.CharField(max_length=20, verbose_name='名称')
    site = models.CharField(max_length=100, verbose_name='会议室位置')
    nums = models.PositiveIntegerField(verbose_name='人数')
    equipment = models.ManyToManyField(MeetingRoomEquipment, verbose_name='设备')
    status = models.PositiveSmallIntegerField(choices=ROOM_STATUS, default=0, verbose_name='状态')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    add_user = models.ForeignKey(user, on_delete=models.DO_NOTHING, verbose_name='添加用户')
    image = models.ImageField(upload_to='meetingroom/', default='liqin.jpg', verbose_name='会议室图片')

    class Meta:
        verbose_name = '会议室信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def equipment_name(self):
        return self.equipment.values_list('name', flat=True)

    @property
    def room_status(self):
        return self.get_status_display()

    @property
    def manager(self):
        return self.add_user.name


class MeetRoomReserve(models.Model):
    """会议室预定"""
    STATUS = (
        (0, '通过'),
        (1, '未通过'),
        (2, '发起'),
        (3, '撤销'),
        (4, '会议未举行')
    )
    name = models.ForeignKey(MeetingRoomInfos, on_delete=models.DO_NOTHING, related_name='room', db_constraint=False,
                             verbose_name='会议室')
    subject = models.CharField(max_length=100, verbose_name='主题')
    begin_datetime = models.DateTimeField(verbose_name='开始时间')
    over_datetime = models.DateTimeField(verbose_name='结束时间')
    chair = models.ForeignKey(user, on_delete=models.DO_NOTHING, related_name='chair', verbose_name='主持人')
    participants = models.ManyToManyField(user, related_name='participant', verbose_name='参与人')
    remarks = models.CharField(max_length=100, verbose_name='备注')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=2, verbose_name='状态')
    approver = models.ForeignKey(user, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='审批人')

    class Meta:
        verbose_name = '会议室预定'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name.name

    @property
    def room_name(self):
        return self.name.name

    @property
    def meeting_chair(self):
        return self.chair.name

    @property
    def meeting_participants(self):
        return ', '.join([participant.name for participant in self.participants.all()])

    @property
    def reserve_status(self):
        return self.get_status_display()

    @property
    def room_approver(self):
        return self.approver.name if self.approver else ''