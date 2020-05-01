from rest_framework.serializers import ModelSerializer
from . import models

class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = models.MeetingRoomInfos
        fields = ['name', 'site', 'nums', 'equipment_name', 'room_status',
                  'add_time', 'manager', 'reserve', 'image'
                  ]
        kwargs = {}