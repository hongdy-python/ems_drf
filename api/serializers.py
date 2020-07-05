from itsdangerous import serializer
from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer

from api.models import User, Employee


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "username":{
                "required":True,
                "min_length":3,
                "error_messages":{
                    "required":"用户名必填",
                    "min_length":"用户名长度不够"
                }
            },
        }

    def validate(self, attrs):
        username = attrs.get("username")
        user = User.objects.filter(username=username).first()
        if user:
            raise exceptions.ValidationError("用户名已存在")
        return attrs

class EmployeeModelSerializer(ModelSerializer):
    class Meta:
        model = Employee
        # fields = "__all__"
        fields = ('id','emp_name','salary','age','age_name','img')

        extra_kwargs = {
            "emp_name": {
                "required": True,
                "min_length": 3,
                "error_messages": {
                    "required": "用户名必填",
                    "min_length": "用户名长度不够"
                }
            },
        }