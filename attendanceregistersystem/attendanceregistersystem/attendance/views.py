from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import MakeAttendanceSerializer, MakeLeaveRequestSerializer, UserDaySerializer
from .permissions import AttendancePermissons
from .models import Attendance, LeaveRequest, UserDays
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localdate, localtime, now
from attendanceregistersystem.users.models  import User



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
    permission_classes = (AllowAny,)
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

    @receiver(post_save, sender=LeaveRequest)
    def post(self, request, *args, **kwargs):
        leave = LeaveRequest.objects.get(user=request.user)
        leave_type =  leave.types_of_leave
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


class MakeLeaveRequest(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MakeLeaveRequestSerializer
    # login_url = '../../users/v1/login/'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


post_save.connect(receiver=UserDay.post, sender=LeaveRequest)


class AcceptRequest(APIView):
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id', 'Default Value if not there')
        leave_request = LeaveRequest.objects.get(pk=pk)
        print(leave_request)
        # if accept :
        #     leave_request.status = 'accept'
        
        # else:
        #     leave_request.status = 'reject'

