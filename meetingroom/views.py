import copy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from . import models
from meetingauth.models import UserProfile
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
            return Response({"message": "请求错误", 'status': 400, 'data': ''})
        rooms_serializer = MeetingRoomSerializer(rooms, many=True)
        return Response({
            'status': 200,
            'message': '获取会议室信息成功',
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
        roomid = kwargs.get('id')
        reserve = models.MeetRoomReserve.objects.filter(name_id=roomid, status__in=[0, 2])
        if roomid and not reserve:
            return Response({
                'status': 200,
                'message': '暂无预订记录',
                'data': ''
            })
        if reserve:
            data = reserve.values_list('begin_datetime', flat=True)
            data_date = set(item for item in data)
            infos = {}
            date_infos = []
            for date in data_date:
                date_infos.append(date.date())
                serializer_data = MeetingReserveSerializer(reserve.filter(begin_datetime__date=date.date()),  many=True)
                infos.setdefault(str(date.date()), serializer_data.data)
            res = {'date': date_infos, 'infos': infos}
            return Response({
                'status': 200,
                'message': '查询会议室预定记录成功',
                'data': res
            })
        reserves = models.MeetRoomReserve.objects.all()
        serializer_reserves = MeetingReserveSerializer(reserves, many=True)
        data = serializer_reserves.data
        return Response({
            'message': "查询会议室预定记录",
            'data': data,
            'status': 200
        })

    def post(self, request, *args, **kwargs):
        """发起一条预定"""
        data = request.data
        room_id = data.get('name')
        room = models.MeetingRoomInfos.objects.filter(id=room_id).first()
        if not room_id or not room:
            return Response({
                'status': 400,
                'message': "会议室预定失败",
                'data': '请求不正确'
            })
        # data.update({'participants': data.get('participants').split(',')})
        chair = UserProfile.objects.get(id=1)

        participants = UserProfile.objects.filter(pk__in=data.get('participants').split(','))
        # 获取同一个会议室，在预定的开始结束，时间之内是否有记录，判断是否可以申请
        begin_datetime = data.get('begin_datetime')
        over_datetime = data.get('over_datetime')

        room = data.get('name')
        if models.MeetRoomReserve.objects.filter(name=room,
                                                 over_datetime__in=[begin_datetime, over_datetime]).exclude(
            status=3).exists():
            raise ValidationError("已经存在预定")
        # 更新attrs数据
        data.update({'chair': chair})
        data.update({'participants': participants})
        reserveSerializer = MeetingReserveSerializer(data=data, context={'request': request})

        reserveSerializer.is_valid(raise_exception=True)
        reserve = reserveSerializer.save()
        return Response({
            'status': 200,
            'message': "会议室预定成功",
            'data': MeetingReserveSerializer(reserve).data
        })

    def patch(self, request, *args, **kwargs):
        """更新预定信息,只更新状态"""
        id = kwargs.get('id')
        reserve = models.MeetRoomReserve.objects.filter(id=id).first()
        data = request.data
        # patch操作只处理状态更新,其他更新方式使用put
        if not reserve or len(data) != 1 or not data.get('status'):
            return Response({'message': '操作失败，请求不正确', 'data': "请求不正确", 'status': 400})
        # 反序列化reserve， partial=True允许局部更新
        reserve_serializer = MeetingReserveSerializer(reserve, data=data, partial=True)
        reserve_serializer.is_valid(raise_exception=True)
        reserve_data = reserve_serializer.save()

        return Response({
            'message': "申请已通过",
            'data': MeetingReserveSerializer(reserve_data).data,
            'status': 200
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