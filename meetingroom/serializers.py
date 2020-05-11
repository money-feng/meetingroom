from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from . import models


class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoomInfos
        fields = ['id', 'name', 'site', 'nums', 'equipment_name', 'room_status',
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
        print(111111111111)
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
            'id': {
                'read_only': True
            }
        }

    def validate(self, attrs):

        # 获取登录用户，也就是预定会议室的用户

        # chair = self.context['request'].user
        return attrs