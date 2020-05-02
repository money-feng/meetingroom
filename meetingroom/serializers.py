from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from . import models


class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoomInfos
        fields = ['name', 'site', 'nums', 'equipment_name', 'room_status',
                  'add_time', 'manager', 'add_user', 'reserve', 'image'
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
