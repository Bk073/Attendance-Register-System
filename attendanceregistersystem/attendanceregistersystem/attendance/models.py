from django.db import models
from attendanceregistersystem.users.models import User
from django.db.models import CharField, IntegerField, EmailField, DateField, AutoField, ForeignKey, CASCADE


class Attendance(models.Model):
    check_in = models.TimeField(auto_now=False, null=True, blank=True)
    check_in_date = models.DateField(auto_now=True)
    check_out = models.TimeField(auto_now=False, null=True, blank=True)
    user = ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()


class TypesOfLeave(models.Model):
    type_id = models.AutoField(primary_key=True)
    leave = {
        ('sick_leave', 'Sick Leave'),
        ('annual_leave', 'Annual Leave'),
    }
    leave_type = models.CharField(max_length=255, choices=leave, null=True, blank=True)

    class Meta:
        default_permissions = ()
    

class LeaveRequest(models.Model):
    leave_id = models.AutoField(primary_key=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    status_choice = {
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    }
    status = models.CharField(max_length=255, choices = status_choice, null=True, blank=True)
    description = models.TextField(null=True, blank=True, help_text="Describe your leave request")
    date_submission = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responded_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name="responded_by")

    class Meta:
        default_permissions = ()

class UserDays(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(TypesOfLeave, on_delete=models.CASCADE)
    days_taken = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        default_permissions = ()