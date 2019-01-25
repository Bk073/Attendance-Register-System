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
        username = view.kwargs['username']
        print(username)
        # user = User.objects.get(id = request.user.id)
        user = User.objects.get(username = username)
        branch = user.branch
        # group = list(user.groups.all())
        
        if  request.user.groups.filter(name='Operational Manager').exists():
            return True
        # permissions = Permission.objects.filter(group__user = request.user).filter(name='can view attendance')
        # return True if permissions.exists() else False
        if Permission.objects.filter(group__user = request.user).filter(name='can view user'):
            if branch == request.user.branch:
                return True
        
        return False

class UpdateUserGroup(BasePermission):
    def has_permission(self, request, view, **kwargs):
        # username = kwargs.get('username', 'Default Value if not there')
        user = User.objects.get(id=request.user.id)

        group = list(user.groups.all())
        print("update group")
        permison = group[0].permissions.all()
        if permison.get(name='can update users group'):
            return True
        else:
            return False


class DeleteUser(BasePermission):
    def has_permission(self, request, view):
        pk = int(view.kwargs['id'])
        # user = User.objects.get(id = request.user.id)
        user = User.objects.get(id = pk)
        branch = user.branch
        # group = list(user.groups.all())
        
        if  request.user.groups.filter(name='Operational Manager').exists():
            return True
        # permissions = Permission.objects.filter(group__user = request.user).filter(name='can view attendance')
        # return True if permissions.exists() else False
        if Permission.objects.filter(group__user = request.user).filter(name='can view leave request'):
            if branch == request.user.branch:
                return True
        
        return False
        