from django.conf.urls import url
from attendanceregistersystem.attendance.views import MakeAttendance

app_name = "attendance"

urlpatterns = [
    url(
        r'^v1/attendance',
        MakeAttendance.as_view(),
        name="make-attendance"
    ),
]