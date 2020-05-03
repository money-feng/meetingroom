from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import jwt_encode_handler

from . import models
from .serializers import MenuListModelSerializer, UserProfileModelSerializer
# Create your views here.


class UserInfosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = kwargs.get('name')
        if query:
            users = models.UserProfile.objects.filter(name__contains=query)
        else:
            users = models.UserProfile.objects.all()
        serializer_users = UserProfileModelSerializer(users, many=True)
        return Response({
            'status': 200,
            'message': "获取用户信息成功",
            'data': serializer_users.data
        })

    def patch(self, request, *args, **kwargs):
        userid = kwargs.get('id')
        user = models.UserProfile.objects.filter(id=userid).first()
        if not (userid and user):
            return Response({
                'status': 400,
                'message': "请求不正确"
            })
        serializer_user = UserProfileModelSerializer(user, data=request.data, partial=True)
        serializer_user.is_valid()
        updated_user = serializer_user.save()
        return Response({
            'status': 200,
            'message': "修改用户信息成功",
            'date': UserProfileModelSerializer(updated_user).data
        })



class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not (username and password):
            return Response({'message': "用户名或密码不能为空"})
        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({
                "message": "欢迎你 {}".format(user.name),
                'status': 200,
                'token': token
            })
        else:
            return Response({
                "message": "账号或者密码不正确",
                'status': 400,
            })

class MenuListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        menus = models.MenuList.objects.filter(parent__isnull=True)
        serializer_data = MenuListModelSerializer(menus, many=True)
        return Response({
            'status': 200,
            'message': "获取菜单成功",
            'data': serializer_data.data
        })