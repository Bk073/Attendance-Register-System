from rest_framework import serializers
from .models import Attendance, LeaveRequest, UserDays, TypesOfLeave
from attendanceregistersystem.users.models import User

class MakeAttendanceSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.all())
    #  user = serializers.ReadOnlyField()
    class Meta:
        model = Attendance
        fields  = ('check_in', 'check_in_date', 'check_out', 'user',)

    
class MakeLeaveRequestSerializer(serializers.Serializer):
    date_to = serializers.DateField()
    date_from = serializers.DateField()
    description = serializers.CharField()
    types_of_leave = serializers.IntegerField()

    def create(self, validated_data):
        user = self.context['request'].user
        print(user)
        print(validated_data['date_to'])
        LeaveRequest.objects.create(user = user)
        return user
    
    def validate_types_of_leave(self, value):
        try:
            self.types_of_leave = TypesOfLeave.objects.get(leave_type_id=value)
        except TypesOfLeave.DoesNotExist:
            self.fail('failed')
         
        return value

class UserDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDays
        fields = ('leave_type', 'days_taken',)