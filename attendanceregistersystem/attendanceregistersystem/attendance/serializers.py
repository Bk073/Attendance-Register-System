from rest_framework import serializers
from .models import Attendance, LeaveRequest
from attendanceregistersystem.users.models import User

class MakeAttendanceSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.all())
    #  user = serializers.ReadOnlyField()
    class Meta:
        model = Attendance
        fields  = ('check_in', 'check_in_date', 'check_out', 'user',)

    
class MakeLeaveRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveRequest
        fields = ('date_from', 'date_to', 'description', 'types_of_leave',)