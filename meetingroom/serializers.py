from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from . import models

class MeetingRoomEquipmentSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoomEquipment
        fields = '__all__'

class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoomInfos
        fields = ['id', 'name', 'site', 'nums', 'equipment', 'equipment_name', 'room_status', 'status',
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
            },
            'equipment': {
                'write_only': True
            }
        }


    def create(self, validated_data):
        kwargs = {
            'name': validated_data.get('name'),
            'site': validated_data.get('site')
        }
        if models.MeetingRoomInfos.objects.filter(**kwargs).exclude(status=3).exists():
            raise ValidationError('会议室已经存在')
        return models.MeetingRoomInfos.objects.create(**kwargs)

    def update(self, instance, validated_data):
        # 将多对多类型的字段先取出来
        equipment = validated_data.pop('equipment')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.equipment.set(equipment)
        instance.save()
        return instance



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