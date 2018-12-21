from django.contrib import admin
from .models import Attendance, TypesOfLeave, LeaveRequest, UserDays

# Register your models here.
admin.site.register(Attendance)
admin.site.register(TypesOfLeave)
admin.site.register(LeaveRequest)