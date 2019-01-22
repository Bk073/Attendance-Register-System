from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from attendanceregistersystem.users.models import User
from attendanceregistersystem.attendance.models import LeaveRequest
from django.contrib.auth.models import Group

class AttendancePermissons(BasePermission):

    def has_permission(self, request, view):
        content_type = ContentType.objects.get_for_model(User)

        if "can make attendance" in Permission.objects.filter(content_type):
            return True
        else:
            return False


class AcceptLeaveRequest(BasePermission):

    def has_permission(self, request, view):
        
        leave_request_id = view.kwargs['id']
        leave_request = LeaveRequest.objects.get(leave_id=int(leave_request_id))
        requested_user = leave_request.user
        om = Group.objects.get(name='Operational Manager')
        user = User.objects.get(username = request.user.username)
        grp = list(user.groups.all())
        branch = user.branch 
        for gp in grp:
            lis = gp.permissions.all()
            if lis.get(name='Can accept leave request'): 
                if branch == requested_user.branch or om in grp : # and branch == leaveRequest send garne user ko branch
                    return True
            else:
                return False


class ViewAttendance(BasePermission):
    def has_permission(self, request, view):
        # print(view.lookup_field)
        # username = view.lookup_field
        # print(username)
        # requested_user = request.user.username
        user = User.objects.get(id = request.user.id)
        branch = user.branch 
        om = Group.objects.get(name='Operational Manager')
        print(user)
        group = list(user.groups.all())
        for grp in group:
            permison = grp.permissions.all()
            # print(permison)
        
            if  permison.get(name='can view attendance'):
                if branch == requested_user.branch or om in group: 
                    return True
            else:
                return False

class ViewUserAttendance(BasePermission):
    def has_permission(self, request, view):
        pk = int(view.kwargs['id'])
        # user = User.objects.get(id = request.user.id)
        user = User.objects.get(id = pk)
        branch = user.branch
        om = Group.objects.get(name='Operational Manager')
        # group = list(user.groups.all())
        if pk == request.user.id:
            return True
            
        if  request.user.groups.filter(name='Operational Manager').exists():
            return True
    
        # permissions = Permission.objects.filter(group__user = request.user).filter(name='can view attendance')
        # return True if permissions.exists() else False
        if Permission.objects.filter(group__user = request.user).filter(name='can view attendance'):
            if branch == request.user.branch:
                return True
        
        return False
    
    


            
            # print(permison.get(name='can view attendance'))
            # try:
            #     permison.get(name='can view attendance')
            #     return True
            # except :
            #     user.id == id
            #     return True
            # else:
            #     return False
            

class ViewUserLeaveRequest(BasePermission):
    def has_permission(self, request, view):
        # group = list(user.groups.all())
        # for grp in group:
        #     permison = grp.permissions.all()
        # # try:
        # #     if  permison.get(name='can view leave request') or user.id == id:
        # #         return True
        # # except :
        # #     return False
        #     try:
        #         permison.get(name='can view leave request')
        #     except :
        #         request.user.id == id
        #         return True
        #     else:
        #         return False
        pk = int(view.kwargs['id'])
        # user = User.objects.get(id = request.user.id)
        user = User.objects.get(id = pk)
        branch = user.branch
        # group = list(user.groups.all())
        if pk == request.user.id:
            return True

        if  request.user.groups.filter(name='Operational Manager').exists():
            return True
        # permissions = Permission.objects.filter(group__user = request.user).filter(name='can view attendance')
        # return True if permissions.exists() else False
        if Permission.objects.filter(group__user = request.user).filter(name='can view leave request'):
            if branch == request.user.branch:
                return True
        
        return False
        

class ViewLeaveRequest(BasePermission):
    def has_permission(self, request, view):
        # requested_user = request.user.username
        user = User.objects.get(id = request.user.id)
        group = list(user.groups.all())
        for grp in group:
            permison = grp.permissions.all()
    
            if permison.get(name='can view leave request'):
                return True
            else:
                return False

class CanAddLeaveType(BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        user = User.objects.get(id = request.user.id)
        group = list(user.groups.all())
        for grp in group:
            permison = group.permissions.all()
    
            if request.method == 'POST' and permison.get(name='can add leave type'):
                return True
            elif request.method == 'GET':
                return True
            else:
                return False
        
        