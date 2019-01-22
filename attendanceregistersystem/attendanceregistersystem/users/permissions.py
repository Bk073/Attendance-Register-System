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
        permison = group[0].permissions.all()
        if permison.get(name='Can add staff'):
            return True
        else:
            return False

class ViewUser(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(id = request.user.id)
        group = list(user.groups.all())
        permison = group[0].permissions.all()
        if permison.get(name='can view user'):
            return True
        else:
            return False

class UpdateUserGroup(BasePermission):
    def has_permission(self, request, view, **kwargs):
        # username = kwargs.get('username', 'Default Value if not there')
        user = User.objects.get(id=request.user.id)

        group = list(user.groups.all())
        permison = group[0].permissions.all()
        if permison.get(name='can update users group'):
            return True
        else:
            return False


class DeleteUser(BasePermission):
    def has_permission(self, request, view, **kwargs):
        user = User.objects.get(id=request.user.id)

        group = list(user.groups.all())
        permison = group[0].permissions.all()
        if permison.get(name='can delete user'):
            return True
        else:
            return False