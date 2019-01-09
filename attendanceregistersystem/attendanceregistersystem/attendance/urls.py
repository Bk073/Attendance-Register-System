from django.conf.urls import url
from attendanceregistersystem.attendance.views import MakeAttendance, MakeLeaveRequest, UserDays, AcceptRequest, UserAttendance, TypesOfLeaveList

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
        r"v1/acceptRequest/(?P<id>\d+)/(?P<status>accept|reject)", #send accept or reject also as kwargs
        AcceptRequest.as_view(),
        name='acceptRequest'
    ),#v1/acceptRequest/1/accept
    url(
        r'v1/view-attendance',
        UserAttendance.as_view(),
        name='viewAttendance'
    ),
    url(
        r'v1/accept-leaveRequest',
        AcceptRequest.as_view(),
        name='viewLeaveRequest'
    ),
    url(
        r'v1/types-of-leave',
        TypesOfLeaveList.as_view(),
        name='TypesOfLeaveList'
    ),
]
