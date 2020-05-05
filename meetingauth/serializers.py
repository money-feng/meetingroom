from rest_framework.serializers import ModelSerializer
from .models import Permission, UserProfile, Roles

class PermissionModelSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'path', 'children', 'style','level']


    def validate(self, attrs):
        print(attrs)
        return attrs


class UserProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'username', 'email', 'phone', 'department_name', 'is_active']

    def validate(self, attrs):
        print(attrs)
        return attrs


class RolesModelSerializer(ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'role_name', 'role_desc', 'role_perms']

