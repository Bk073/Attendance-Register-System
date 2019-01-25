from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.views import LoginView
from .serializers import UserLoginSerializers, UserSerializers, UserSerializersDefault, GroupSerializer, PermissionSerializer, BranchSerializers, UserSerializer, UserUpdateSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
User = get_user_model()
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models.signals import post_save
from django.utils.timezone import localdate, localtime, now
from djoser.views import TokenDestroyView
from .permissions import CreateNewStaff, ViewUser, UpdateUserGroup, DeleteUser
from djoser import utils
from .models import Branch
from django.contrib.auth.models import Group, Permission
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

# use generics. views
# previously used ModelViewSet

# class UserCreateView(generics.CreateAPIView):
#     permission_classes = (CreateNewStaff,)
#     # serializer_class = UserSerializers
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer_class(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#     def get_serializer_class(self):
#         user = User.objects.get(username = self.request.user.username)
#         if user.groups == 'Operational Manager':
#             return UserSerializers
#         else:
#             return UserSerializersDefault

class UserCreateView(generics.CreateAPIView):
    permission_classes = (CreateNewStaff,)
    # permission_classes = (AllowAny,)
    serializer_class = UserSerializers

user_create_view = UserCreateView.as_view()

class UserListView(generics.ListAPIView):
    # permission_classes= (ViewUser,)
    permission_classes = (AllowAny,)
    # permission_classes= (IsAuthenticated,)
    serializer_class = UserSerializer
    # queryset = User.objects.all()
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        group = list(user.groups.all())
        print(group[0])
        om = Group.objects.get(name='Operational Manager')
        if om in group:
            queryset= User.objects.all()
            print("hello")
            return queryset
        else:
            queryset= User.objects.filter(branch=user.branch)
            return queryset
        


user_list_view = UserListView.as_view()


class UserDetailView(generics.RetrieveAPIView):

    # model = User
    # slug_field = "username"
    # slug_url_kwarg = "username"
    lookup_field = 'username'
    # lookup_url_kwarg ='username'
    permission_classes = (ViewUser,)
    # permission_classes = (AllowAny,)  
    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        # username = self.lookup_field
        queryset = User.objects.filter(username = username)
        return queryset

user_detail_view = UserDetailView.as_view()


# class UserListView(LoginRequiredMixin, ListView):

    
#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"


# user_list_view = UserListView.as_view()


# class UserUpdateView(APIView):
#     # serializer_class = UserSerializers
#     permission_classes = (IsAuthenticated, )
#     lookup_field = 'username'

#     def get_object(self, username):
#         try:
#             return User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise Http404

#     def put(self, request, username, format=None):
#         user = self.get_object(username)
#         serializer = UserSerializers(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(GenericAPIView, UpdateModelMixin):
    serializer_class = UserSerializers  
    permission_classes = (IsAuthenticated, )  
    queryset = User.objects.all()
    # lookup_field = 'username'

    # def partial_update(self, request, pk=None):
    #     serialized = UserSerializers(request.user, data=request.data, partial=True)
    #     return Response(status=status.HTTP_202_ACCEPTED)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# user_update_view = UserUpdateView.as_view({'get': 'retrieve', 'patch':'partial_update'})
user_update_view = UserUpdateView.as_view()

# class UserGroupUpdateView(GenericAPIView, UpdateModelMixin):
#     serializer_class = UserUpdateSerializer  
#     permission_classes = (UpdateUserGroup, )  
#     # queryset = User.objects.all()
#     lookup_field = 'pk'

#     # def partial_update(self, request, pk=None):
#     #     serialized = UserSerializers(request.user, data=request.data, partial=True)
#     #     return Response(status=status.HTTP_202_ACCEPTED)
#     def patch   (self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
    
#     def get_queryset(self):
#         print("hello")
#         id = self.kwargs['pk']
#         queryset = User.objects.filter(id = id)
#         print(queryset)
#         return queryset

class UserGroupUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer  
    permission_classes = (UpdateUserGroup, )  
    queryset = User.objects.all()

# user_update_view = UserUpdateView.as_view({'get': 'retrieve', 'patch':'partial_update'})
user_group_update_view = UserGroupUpdateView.as_view()


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
        Attendance.objects.get_or_create(user=user, check_in_date=localdate(now())) 
        #Attendance.objects.get_or_create()
        #django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)

user_login_view = UserLoginView.as_view()

post_save.connect(MakeAttendance.make_attendance, sender=Token)



class UserLogoutView(TokenDestroyView):

    def post(self, request):
        print("Hello djoser")
        attendance = Attendance.objects.get(user=request.user, check_in_date=localdate(now()))
        attendance.check_out = localtime(now())
        attendance.save()
        print(attendance)
        print(attendance.check_out)
        utils.logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
user_logout_view = UserLogoutView.as_view()

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


class GroupCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GroupSerializer
    # login_url = '../../users/v1/login/'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        data = serializer.save()
        print(data)
        # headers = self.get_success_headers(serializer.data)
        return Response({'ok':'ok'}, status=status.HTTP_201_CREATED)


groups_create_view = GroupCreateView.as_view()

class PermissionCreateView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    # login_url = '../../users/v1/login/'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        data = serializer.save()
        print(data)
        # headers = self.get_success_headers(serializer.data)
        return Response({'ok':'ok'}, status=status.HTTP_201_CREATED)


permission_create_view = PermissionCreateView.as_view()

class BranchList(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializers


branch_list_view = BranchList.as_view()

    
class GroupList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


groups_list_view = GroupList.as_view()


class UserDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializers
    permission_classes = (DeleteUser,)
    lookup_url_kwarg = "id"
    queryset = User.objects.all()


    # def get_object(self):
    #     # id = kwargs.get('id', 'Default Value if not there') # yo id user ko ho ki leave request model ko ?
        
    #     id=self.kwargs.get(self.lookup_url_kwarg)
    #     user = User.objects.get(id=id)
    #     print(user)
    #     queryset = LeaveRequest.objects.get(user=user)
    #     print(queryset)
    #     return queryset


user_delete_view = UserDeleteView.as_view()