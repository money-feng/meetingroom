from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .serializers import MeetingRoomSerializer
# Create your views here.


class MeetingRoomApiView(APIView):
    def get(self, request, *args, **kwargs):
        """获取所有可用会议室或单个会议室"""
        meeting_room_id = kwargs.get('id')
        if meeting_room_id:
            rooms = models.MeetingRoomInfos.objects.filter(pk=meeting_room_id,
                                        status=0, reserve_status=0)
        else:
            rooms = models.MeetingRoomInfos.objects.filter(status=0, reserve_status=0)
        if not rooms.exists():
            return Response({"message": "请求错误"})
        rooms_serializer = MeetingRoomSerializer(rooms, many=True)
        return Response({
            'status': 200,
            'message': 'success',
            'data': rooms_serializer.data
        })

    def post(self, request, *args, **kwargs):
        """增加一条数据"""
        data = request.data
        print('------>', data)
        rooms_serializer = MeetingRoomSerializer(data=data)
        rooms_serializer.is_valid(raise_exception=True)
        room = rooms_serializer.save()
        return Response({
            'message': '增加会议室',
            'data': MeetingRoomSerializer(room).data
        })

    def patch(self, request, *args, **kwargs):
        """更新一条数据"""
        meeting_room_id = kwargs.get('id')
        data = request.data
        meeting_room = models.MeetingRoomInfos.objects.filter(pk=meeting_room_id).first()
        if not meeting_room_id or not data or not meeting_room:
            return Response({
                "message": "修改会议室",
                "data": "请求不正确"
            })
        rooms_serializer = MeetingRoomSerializer(meeting_room, data=data, partial=True)
        rooms_serializer.is_valid()
        room = rooms_serializer.save()
        return Response({
            'message': '修改会议室',
            'data': MeetingRoomSerializer(room).data
        })

    def delete(self, request, *args, **kwargs):
        """删除一条数据(这里采用更改状态的方式)"""
        meeting_room_id = kwargs.get('id')
        meeting_room = models.MeetingRoomInfos.objects.filter(pk=meeting_room_id)
        if not meeting_room_id or not meeting_room:
            return Response({
                "message": "修改会议室",
                "data": "请求不正确"
            })
        meeting_room.update(status=3)
        return Response({
            "message": "删除会议室",
            "data": "删除完成"
        })

class MeetingRoomRecordsApiView(APIView):
    """处理会议室申请"""
    def get(self, request, *args, **kwargs):
        pass