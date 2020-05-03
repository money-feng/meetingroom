from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .serializers import MeetingRoomSerializer, MeetingReserveSerializer
# Create your views here.


class MeetingRoomApiView(APIView):
    def get(self, request, *args, **kwargs):
        """获取所有可用会议室或单个会议室"""
        meeting_room_id = kwargs.get('id')
        if meeting_room_id:
            rooms = models.MeetingRoomInfos.objects.filter(pk=meeting_room_id,
                                        status=0)
        else:
            rooms = models.MeetingRoomInfos.objects.filter(status=0)
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

class MeetingRecordsApiView(APIView):
    """处理会议室申请"""
    def get(self, request, *args, **kwargs):
        """查看申请记录"""
        reserves = models.MeetRoomReserve.objects.all()
        serializer_reserves = MeetingReserveSerializer(reserves, many=True)
        data = serializer_reserves.data
        return Response({
            'message': "查询会议室预定记录",
            'data': data
        })

    def post(self, request, *args, **kwargs):
        """发起一条预定"""
        data = request.data
        room_id = data.get('id')
        room = models.MeetingRoomInfos.objects.filter(id=room_id).first()
        if not room_id or not room:
            return Response({
                'message': "会议室预定",
                'data': '请求不正确'
            })
        data.update({'name': room})
        reserveSerializer = MeetingReserveSerializer(data=data, context={'request': request})
        reserveSerializer.is_valid(raise_exception=True)
        reserve = reserveSerializer.save()
        return Response({
            'message': "会议室预定",
            'data': MeetingReserveSerializer(reserve).data
        })

    def patch(self, request, *args, **kwargs):
        """更新预定信息,只更新状态"""
        id = kwargs.get('id')
        reserve = models.MeetRoomReserve.objects.filter(id=id).first()
        data = request.data
        # patch操作只处理状态更新,其他更新方式使用put
        if not reserve or len(data) != 1 or not data.get('status'):
            return Response({'message': '预定更新', 'data': "请求不正确"})
        # 反序列化reserve， partial=True允许局部更新
        reserve_serializer = MeetingReserveSerializer(reserve, data=data, partial=True)
        reserve_serializer.is_valid(raise_exception=True)
        reserve_data = reserve_serializer.save()

        return Response({
            'message': "预定更新",
            'data': MeetingReserveSerializer(reserve_data).data
        })

    def put(self, request, *args, **kwargs):
        """更新预定信息，需要提供全部数据"""
        id = kwargs.get('id')
        reserve = models.MeetRoomReserve.objects.filter(id=id).first()
        data = request.data
        data.update({'name': reserve.name.id})
        if not data or not reserve:
            return Response({'message': '预定更新', 'data': "请求不正确"})
        reserve_serializer = MeetingReserveSerializer(reserve, data=data)
        reserve_serializer.is_valid(raise_exception=True)
        reserve_data = reserve_serializer.save()
        return Response({
            'message': "预定更新",
            'data': MeetingReserveSerializer(reserve_data).data
        })

    def delete(self, request, *args, **kwargs):
        """删除预定记录"""
        id = kwargs.get('id')
        reserve = models.MeetRoomReserve.objects.filter(id=id).first()
        if not reserve:
            return Response({'message': '预定更新', 'data': "请求不正确"})
        reserve.delete()
        return Response({
            "message": "预定删除",
            "data": "删除完成"
        })