from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import jwt_encode_handler

from . import models
from .serializers import PermissionModelSerializer, UserProfileModelSerializer, RolesModelSerializer
# Create your views here.


class UserInfosAPIView(APIView):
    """操作用户的view"""
    def get(self, request, *args, **kwargs):
        """获取全部或者部分用户"""
        query = kwargs.get('query')
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

    def post(self, request, *args, **kwargs):
        """添加用户信息"""
        data = request.data
        serializer_user = UserProfileModelSerializer(data=data)
        serializer_user.is_valid()
        user= serializer_user.save()
        return Response({
            "status": 201,
            "message": "添加用户完成",
            "data": UserProfileModelSerializer(user).data
        })

    def patch(self, request, *args, **kwargs):
        """更新用户，部分更新"""
        userid = kwargs.get('query')
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

    def delete(self, request, *args, **kwargs):
        """删除用户"""
        userid = kwargs.get('query')
        user = models.UserProfile.objects.filter(id=userid).first()
        if not (userid and user):
            return Response({
                'status': 400,
                'message': "请求不正确"
            })
        user.delete()
        return Response({
            'status': 200,
            'message': "删除用户信息成功",
            'date': ""
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

class PermissionPIView(APIView):
    def get(self, request, *args, **kwargs):
        type = request.query_params.get('type')
        if type == 'list':
            perms = models.Permission.objects.all().values()
            return Response({
                'status': 200,
                'message': "获取菜单成功",
                'data': perms
            })
        perms = models.Permission.objects.filter(level=0)
        serializer_data = PermissionModelSerializer(perms, many=True)
        return Response({
            'status': 200,
            'message': "获取菜单成功",
            'data': serializer_data.data
        })


class RolsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        roles = models.Roles.objects.all()
        serializer_roles = RolesModelSerializer(roles, many=True)
        return Response({
            'status': 200,
            'message': "获取角色成功",
            'data': serializer_roles.data
        })

    def delete(self, request, *args, **kwargs):
        roleid = kwargs.get('query')
        permid = request.data.get('permid')
        print(permid)
        role = models.Roles.objects.filter(id=roleid).first()
        perm = models.Permission.objects.filter(id=permid).first()
        if not (role and perm):
            return Response({
                'status': 400,
                'message': "请求不正确",
                'data': ''
            })
        print(role.permissions.all())
        # roles = models.Roles.objects.all()
        # serializer_roles = RolesModelSerializer(roles, many=True)
        return Response({
            'status': 200,
            'message': "删除角色成功",
            'data': 1
        })