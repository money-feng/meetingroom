from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from . import models
from meetingauth.models import UserProfile

class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoomInfos
        fields = ['name', 'site', 'nums', 'equipment_name', 'room_status',
                  'add_time', 'manager', 'add_user', 'image'
                  ]
        extra_kwargs = {
            'name': {
                'required': True,
                'error_messages': {
                    'required': '会议室名称不能为空'
                }
            },
            'image': {
                'required': False
            },
            'add_user': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        kwargs = {
            'name': attrs.get('name'),
            'site': attrs.get('site')
        }
        if models.MeetingRoomInfos.objects.filter(**kwargs).exclude(status=3).exists():
            raise ValidationError('会议室已经存在')
        return attrs


class MeetingReserveSerializer(ModelSerializer):
    class Meta:
        model = models.MeetRoomReserve
        fields = ['id', 'name','room_name', 'subject', 'begin_datetime', 'over_datetime', 'meeting_chair',
                  'meeting_participants', 'remarks', 'status', 'reserve_status', 'room_approver']

        extra_kwargs = {
            'name': {
                'write_only': True,
                'required': False
            },
            'status': {
                'write_only': True
            },
            'id': {
                'read_only': True
            }
        }
    def validate(self, attrs):

        # 获取登录用户，也就是预定会议室的用户
        # chair = self.context['request'].user
        chair = UserProfile.objects.get(id=1)
        # 获取同一个会议室，在预定的开始结束，时间之内是否有记录，判断是否可以申请
        begin_datetime = attrs.get('begin_datetime')
        over_datetime = attrs.get('over_datetime')
        room = attrs.get('name')
        if models.MeetRoomReserve.objects.filter(name=room,
        over_datetime__in=[begin_datetime, over_datetime ]).exclude(status=3).exists():
            raise ValidationError("已经存在预定")
        # 更新attrs数据
        attrs.update({'chair': chair})

        return attrs