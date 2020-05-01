from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .serializers import MeetingRoomSerializer
# Create your views here.


class MeetingRoomApiView(APIView):
    def get(self, request, *args, **kwargs):
        rooms = models.MeetingRoomInfos.objects.filter(status=0, reserve_status=0)
        rooms_serializer = MeetingRoomSerializer(rooms, many=True)
        return Response({
            'status': 200,
            'message': 'success',
            'data': rooms_serializer.data
        })

    def post(self, request, *args, **kwargs):
        data = request.data
        rooms_serializer = MeetingRoomSerializer(data=data)
        rooms_serializer.is_valid()
        return Response({
            'message': '增加会议室',
            'data': rooms_serializer.data
        })