from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import MakeAttendanceSerializer, MakeLeaveRequestSerializer, UserDaySerializer, TypesOfLeaveSerializer, LeaveRequestSerializer
from .permissions import AttendancePermissons, AcceptLeaveRequest, ViewUserAttendance
from .models import Attendance, LeaveRequest, UserDays, TypesOfLeave
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localdate, localtime, now
from attendanceregistersystem.users.models  import User, Branch
from rest_framework.response import Response



# class MakeAttendance(generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = MakeAttendanceSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)

class MakeAttendance(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MakeAttendanceSerializer
    # def perform_create(self, serializer_class):
    #     serializer_class.save(user= self.request.user)
    @receiver(post_save, sender=Token)
    def make_attendance(instance, sender ,**kwargs):
        attendance = Attendance.objects.get(user=instance.user, check_in_date=localdate(now()))
        attendance.check_in = localtime(now())
        # print(attendance.check_in_date)
        attendance.save()


class UserDay(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    # @receiver(post_save, sender=LeaveRequest)
    def post(self, request, *args, **kwargs):
        leave_reqs = LeaveRequest.objects.filter(user=request.user)
        leave_type =  leave_req.types_of_leave
        days = leave.date_from - leave.date_to
        user_leave = UserDays.objects.get_or_create(user = request.user, leave_type=leave_type)
        user_leave.days_taken = TypesOfLeave.get(leave_type=leave_type).total_days - days
        user_leave.save()


class UserDays(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserDaySerializer
    queryset = UserDays.objects.all()


class UserAttendance(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MakeAttendanceSerializer
    queryset = Attendance.objects.all()


class UsernameAttendance(generics.RetrieveAPIView):
    permission_classes = (ViewUserAttendance,)
    serializer_class = MakeAttendanceSerializer
    lookup_field = 'username'
    queryset = Attendance.objects.all()


class MakeLeaveRequest(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MakeLeaveRequestSerializer
    # login_url = '../../users/v1/login/'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
        # self.perform_create(serializer)
            date = serializer.save()
            print(date)
        # headers = self.get_success_headers(serializer.data)
        return Response({'ok':'ok'}, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        print(request)
        resp = self.create(request, *args, **kwargs)
        print(resp)
        return resp

# post_save.connect(receiver=UserDay.post, sender=LeaveRequest)


class AcceptRequest(APIView):
    permission_classes = (AcceptLeaveRequest,)

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id', 'Default Value if not there') # yo id user ko ho ki leave request model ko ?
        statu = kwargs.get('status', 'Default Value if not there')
        leave_request = LeaveRequest.objects.get(leave_id=id)
        if statu == 'accept' :
            leave_request.status = 'Approved'
        else:
            leave_request.status = 'Rejected'
            
        print(leave_request.status)
        leave_request.save()
        
        return Response({'ok':'ok'}, status=status.HTTP_201_CREATED)

    # def get(self, request, format=None):
    #     leave_request = LeaveRequest.objects.all()
    #     return Response(leave_request)


class  TypesOfLeaveList(generics.ListCreateAPIView):
    queryset = TypesOfLeave.objects.all()
    serializer_class = TypesOfLeaveSerializer
    permission_classes = (AllowAny,)


class LeaveRequestList(generics.ListAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = (AllowAny,)

    