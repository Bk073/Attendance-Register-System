from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from attendanceregistersystem.users.models import User


class CreateNewStaff(BasePermission):

    def has_permission(self, request, view):
        # content_type = ContentType.objects.get_for_model(User)
        # content_type = content_type.groups
        user = User.objects.get(id = request.user.id)
        group = list(user.groups.all()) #changing queryset to list
        # if group[0].permissions.get(name='Can add staff'):
        permison = list(group[0].permissions.all())
        if permison.get(name='Can add staff'):
            return True
        else:
            return False