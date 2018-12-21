from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import MakeAttendanceSerializer


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

    def perform_create(self, serializer_class):
        serializer_class.save(user= self.request.user)
