from django.conf.urls import url
from attendanceregistersystem.attendance.views import MakeAttendance, LeaveRequestList, MakeLeaveRequest, UserDaysLeft, AcceptRequest, UserAttendance, TypesOfLeaveList, UsernameAttendance, UserLeaveRequest, UserDateAttendance, DateAttendance

app_name = "attendance"
    
urlpatterns = [
    url(
        r'^v1/attendance/$',
        MakeAttendance.as_view(),
        name="make-attendance"
    ),
    url(
        r'^v1/leaveRequest/$',
        MakeLeaveRequest.as_view(),
        name="make-leave-request"
    ),
    url(
        r'^v1/leaveRequestList/$',
        LeaveRequestList.as_view(),
        name="leave-request-list"
    ),
    url(
        r'^v1/leaveRequestList/(?P<id>\d+)/$',
        UserLeaveRequest.as_view(),
        name="user-leave-request-list"
    ),
    url(
        r'^v1/userdays/$',
        UserDaysLeft.as_view(),
        name="userdays"
    ),
    url(
        r'^v1/userdays/(?P<id>\d+)/(?P<leavetype>\w+)/$',
        UserDaysLeft.as_view(),
        name="userdays"
    ),
    url(
        r"v1/acceptRequest/(?P<id>\d+)/(?P<status>accept|reject)", #send accept or reject also as kwargs
        AcceptRequest.as_view(),
        name='acceptRequest'
    ),#v1/acceptRequest/1/accept
    url(
        r'v1/view-attendance/$',
        UserAttendance.as_view(),
        name='viewAttendance'
    ),
    url(
        # r'v1/view-user-attendance/(?P<username>\w+)/$', #attend/v1/view-user-attendance/bishwa/
        r'v1/view-user-attendance/(?P<id>\d+)/$',
        UsernameAttendance.as_view(),
        name='viewAttendance'
    ),
    url(
        r'v1/accept-leaveRequest',
        AcceptRequest.as_view(),
        name='viewLeaveRequest'
    ),
    url(
        r'v1/types-of-leave/$',
        TypesOfLeaveList.as_view(),
        name='TypesOfLeaveList'
    ),
    url(
        r'v1/attendance-date-wise/$',
        DateAttendance.as_view(),
        name='Datewise attendance'
    ), 
    url(
        r'v1/user-attendance-date-wise/$',
        UserDateAttendance.as_view(),
        name='User Datewise attendance'
    ),
]
