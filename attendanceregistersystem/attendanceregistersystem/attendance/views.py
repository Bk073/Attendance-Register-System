from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import MakeAttendanceSerializer, MakeLeaveRequestSerializer
from .permissions import AttendancePermissons
from .models import Attendance, LeaveRequest
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localdate, localtime, now

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


class MakeLeaveRequest(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MakeLeaveRequestSerializer
    # login_url = '../../users/v1/login/'
