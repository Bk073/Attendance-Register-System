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

    def has_permission(self, request, view):
        user = User.objects.get(username = request.user.username)
        grp = list(user.groups.all())
        lis = grp[0].permissions.all()
        if lis.get(name='Can accept leave request'):
            return True
        else:
            return False