from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.views import LoginView
from rest_framework import generics
from .serializers import UserLoginSerializers, UserSerializers
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny
User = get_user_model()
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models.signals import post_save
from django.utils.timezone import localdate, localtime, now

# use generics. views
# previously used ModelViewSet

class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializers
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


user_create_view = UserCreateView.as_view()


class UserListView(generics.ListAPIView):
    permission_classes= (AllowAny,)
    serializer_class = UserSerializers
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return user.groups.all()


user_list_view = UserListView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


# class UserListView(LoginRequiredMixin, ListView):

    
#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"


# user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


from rest_framework.views import APIView
from django.contrib.auth import login as django_login
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from attendanceregistersystem.attendance.models import Attendance
from attendanceregistersystem.attendance.views import MakeAttendance

class UserLoginView(APIView):
    permission_classes = (AllowAny,) 
    authentication_classes = (TokenAuthentication,) 

    def post(self, request):
        serializer = UserLoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]   
        # get Attendance object and save check_in_time and data
        # get this attendance object and update check_out when checkouts
        # a = Attendance.objects.get(user=request.user)
        # a.check_out = time
        # a.save()
        #Attendance.objects.get_or_create()
        Attendance.objects.get_or_create(user=user, check_in_date=localdate(now())), 
        #Attendance.objects.get_or_create()
        #django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)

user_login_view = UserLoginView.as_view()

post_save.connect(MakeAttendance.make_attendance, sender=Token)

# from django.contrib.auth import authenticate
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.status import (
#     HTTP_400_BAD_REQUEST,
#     HTTP_404_NOT_FOUND,
#     HTTP_200_OK
# )
# from rest_framework.response import Response


# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#     if username is None or password is None:
#         return Response({'error': 'Please provide both username and password'},
#                         status=HTTP_400_BAD_REQUEST)
#     user = authenticate(username=username, password=password)
#     if not user:
#         return Response({'error': 'Invalid Credentials'},
#                         status=HTTP_404_NOT_FOUND)
#     token, _ = Token.objects.get_or_create(user=user)
#     return Response({'token': token.key},
#                     status=HTTP_200_OK)


