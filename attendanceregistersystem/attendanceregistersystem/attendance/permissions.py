from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from attendanceregistersystem.users.models import User

class AttendancePermissons(BasePermission):

    def has_permission(self, request, view):
        content_type = ContentType.objects.get_for_model(User)

        if "can make attendance" in Permission.objects.filter(content_type):
            return True
        else:
            return False


class AcceptLeaveRequest(BasePermission):

    def has_permission(self, request, view, *args, **kwargs):
        leave_request_id = kwargs.get('id', 'Default Value if not there')
        requested_user = leave_request_id.user
        user = User.objects.get(username = request.user.username)
        grp = list(user.groups.all())
        lis = grp[0].permissions.all()
        branch = user.branch 
        if lis.get(name='Can accept leave request') and  branch == requested_user.branch: # and branch == leaveRequest send garne user ko branch
            return True
        else:
            return False


class ViewUserAttendance(BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        username = kwargs.get('username', 'Default Value if not there')
        requested_user = request.user.username
        user = User.objects.get(id = request.user.id)
        group = list(user.groups.all())
        permison = group[0].permissions.all()
    
        if username == requested_user:
            return True
        elif  permison.get(name='can view attendance'):
            return True
        else:
            return False