from django.conf.urls import url
from attendanceregistersystem.attendance.views import MakeAttendance, MakeLeaveRequest, UserDays, AcceptRequest

app_name = "attendance"

urlpatterns = [
    url(
        r'^v1/attendance',
        MakeAttendance.as_view(),
        name="make-attendance"
    ),
    url(
        r'^v1/leaveRequest',
        MakeLeaveRequest.as_view(),
        name="make-leave-request"
    ),
    url(
        r'^v1/userdays',
        UserDays.as_view(),
        name="userdays"
    ),
    url(
        r'v1/acceptRequest/<int:pk>',
        AcceptRequest.as_view(),
        name='acceptRequest'
    ),
]