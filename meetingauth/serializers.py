from rest_framework.serializers import ModelSerializer
from .models import MenuList, UserProfile

class MenuListModelSerializer(ModelSerializer):
    class Meta:
        model = MenuList
        fields = ['id', 'name', 'path', 'children', 'style']


    def validate(self, attrs):
        print(attrs)
        return attrs


class UserProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'phone', 'department_name', 'is_active']