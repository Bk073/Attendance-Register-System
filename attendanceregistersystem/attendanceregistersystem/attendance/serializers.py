from rest_framework import serializers
from attendanceregistersystem.attendance.models import Attendance, LeaveRequest, UserDays, TypesOfLeave
from attendanceregistersystem.users.models import User
from django.core.exceptions import ObjectDoesNotExist
from attendanceregistersystem.users.serializers import UserSerializers

class MakeAttendanceSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.all())
    #  user = serializers.ReadOnlyField()
    check_in = serializers.TimeField(format="%H:%M:%S")
    check_out = serializers.TimeField(format="%H:%M:%S")
    user = UserSerializers()
    class Meta:
        model = Attendance
        fields  = ('check_in', 'check_in_date', 'check_out', 'user',)


class MakeLeaveRequestSerializer(serializers.ModelSerializer):
    # date_to = serializers.DateField()
    # date_from = serializers.DateField()
    # description = serializers.CharField()
    # types_of_leave = serializers.IntegerField()
    class Meta:
        model = LeaveRequest
        fields = ( 'date_to', 'date_from', 'description', 'types_of_leave',)

    def create(self, validated_data):
        user = self.context['request'].user # in view self.request and in serializer self.context 
        print(user.username)   
        print(validated_data['date_to'])
        req = LeaveRequest.objects.create(user=User.objects.get(username=user.username))
        req.date_to = validated_data['date_to']  
        req.date_from = validated_data['date_from']       
        req.description = validated_data['description']
        req.types_of_leave = validated_data['types_of_leave']  
        print(req.types_of_leave)
        leave = req.save()
        return req                 
    # def save(self, **kwargs):
    #     user = self.context['request'].user
    #     LeaveRequest.objects.create(user=user)
    
    # def validate_types_of_leave(self, value):
    #     try:
    #         self.types_of_leave = TypesOfLeave.objects.get(leave_type_id=value)
    #     except TypesOfLeave.DoesNotExist:
    #         self.fail('failed')
         
    #     return value




class TypesOfLeaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypesOfLeave
        fields = ('leave_type_id', 'leave_type', 'total_days',)
    

class LeaveRequestSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    types_of_leave = TypesOfLeaveSerializer()
    class Meta:
        model = LeaveRequest
        fields = ('leave_id','date_to', 'date_from', 'description', 'types_of_leave', 'status', 'date_submission', 'user')


class UserDaySerializer(serializers.ModelSerializer):
    user = UserSerializers()
    leave_type = TypesOfLeaveSerializer()
    class Meta:
        model = UserDays
        fields = ('leave_type','user', 'days_left',)