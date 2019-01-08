from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from attendanceregistersystem.users.models import User


class CreateNewStaff(BasePermission):

    def has_permission(self, request, view):
        content_type = ContentType.objects.get_for_model(User)
        content_type = content_type.objects.groups.all()

        if "Can add staff" in Permission.objects.filter(content_type):
            return True
        else:
            return False