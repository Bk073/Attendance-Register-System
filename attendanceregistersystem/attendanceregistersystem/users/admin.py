from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from attendanceregistersystem.users.forms import UserChangeForm, UserCreationForm
from .models import User, Branch, Attendance, TypesOfLeave, LeaveRequest, UserDays

admin.site.register(User)
admin.site.register(Branch)
admin.site.register(Attendance)
admin.site.register(TypesOfLeave)
admin.site.register(LeaveRequest)

admin.site.register(Permission)