from django.conf.urls import url
from attendanceregistersystem.attendance.views import MakeAttendance, MakeLeaveRequest

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
]