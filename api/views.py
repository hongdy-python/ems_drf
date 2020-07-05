from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from api.models import User, Employee
from api.serializers import UserModelSerializer, EmployeeModelSerializer
from utils.response import APIResponse


class Userinfor(APIView):
    def post(self,request,*args,**kwargs):
        request_data = request.data
        print(request_data)
        print(request_data.get("password"),request_data.get("re_password"))
        pwd = request_data.get("password")
        re_pwd = request_data.get("re_password")
        if pwd == re_pwd:
            serializer = UserModelSerializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            user_obj = serializer.save()
            return APIResponse(200,True, results = UserModelSerializer(user_obj).data)
        return APIResponse(400,False,)

    def get(self,request,*args,**kwargs):
        username = request.query_params.get('username')
        password = request.query_params.get('password')
        user = User.objects.filter(username=username,password=password).first()
        if user:
            data = UserModelSerializer(user).data
            return APIResponse(200,True,results=data)
        return APIResponse(400,False)

class EmployeeView(GenericAPIView,ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeModelSerializer
    lookup_field = 'id'
    def get(self,request,*args,**kwargs):
        emp_id = kwargs.get('id')
        # print(emp_id,666)
        if emp_id:
            user_list = self.retrieve(request,*args,**kwargs)
        else:
            user_list = self.list(request,*args,**kwargs)
        return APIResponse(200,True,results=user_list.data)

    def post(self,request,*args,**kwargs):
        # data = request.data
        # self.create()
        user_obj = self.create(request,*args,**kwargs)
        return APIResponse(200,True,results=user_obj.data)

    def patch(self,request,*args,**kwargs):

        user_obj = self.partial_update(request,*args,**kwargs)
        print(user_obj,123)
        return APIResponse(200,True,results=user_obj.data)

    def delete(self,request,*args,**kwargs):
        print(1)
        self.destroy(request,*args,**kwargs)
        print(123)
        return APIResponse(200,True)



