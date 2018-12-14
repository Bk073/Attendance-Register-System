from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, IntegerField, EmailField, DateField, AutoField, ForeignKey, CASCADE
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

def validate_number(contact):
    if contact != 13:
        raise ValidationError(
            f'{contact} not correct format'
        )


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_choice = {
        ('supervisor', 'Supervisor'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    }
    role = models.CharField(max_length=255, choices=role_choice)


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=255,blank=False, null=False, default='Management')

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    user_id = AutoField(primary_key=True)
    first_name = CharField(_("First name of User"), blank=True, max_length=255)
    last_name = CharField(_("Last name of User"), blank=True, max_length=255)
    address = CharField(blank=True, max_length=255)
    # password = CharField(max_length=50)
    contact = PhoneNumberField(validators=[validate_number], max_length=13, help_text="Enter phone number with country code", null=True)
    #phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', 
    #                            error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    email = EmailField(blank=True, null=True, verbose_name="Email")
    date_of_birth = DateField(blank=True, null=True)
    #role_id = ForeignKey('Role', on_delete=CASCADE)
    branch = ForeignKey(Branch, on_delete=CASCADE, default='Management')

    class Meta:
        permissions = (
            ("add_staff", "Can add staff"),
            ("accept_request", "Can accept leave request"),
            ("make_request", "can make leave request"),
            ("set_roles_of_staff", "can set roles of staff"),
            ("view_attendance", "can veiw attendance"),
        )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Attendance(models.Model):
    check_in = models.TimeField(auto_now=True)
    check_in_date = models.DateField(auto_now=True)
    check_out = models.TimeField(auto_now=True)
    user = ForeignKey(User, on_delete=models.CASCADE)


class TypesOfLeave(models.Model):
    type_id = models.AutoField(primary_key=True)
    leave = {
        ('sick_leave', 'Sick Leave'),
        ('annual_leave', 'Annual Leave'),
    }
    leave_type = models.CharField(max_length=255, choices=leave, null=True, blank=True)


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


class UserDays(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(TypesOfLeave, on_delete=models.CASCADE)
    days_taken = models.IntegerField(null=False, blank=False, default=0)