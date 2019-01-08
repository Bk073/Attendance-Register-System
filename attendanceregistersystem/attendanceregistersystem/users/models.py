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

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=255,blank=True, null=True)

    class Meta:
        default_permissions = ()
    
    def get_absolute_url(self):
        return reverse("branch:detail", kwargs={"branchname": self.branch_name})
   
    def __str__(self):
        return '%s' % (self.branch_name)

    # def get_absolute_url(self):
    #     return reverse("branch:detail", kwargs={"name": self.name})

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    id = AutoField(primary_key=True)
    first_name = CharField(_("First name of User"), blank=True, max_length=255)
    last_name = CharField(_("Last name of User"), blank=True, max_length=255)
    address = CharField(blank=True, max_length=255)
    # password = CharField(max_length=50)
    # contact = PhoneNumberField( max_length=13, help_text="Enter phone number with country code", null=True, blank=True)
    #phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', 
    #                            error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    contact = IntegerField(max_length=13, help_text="Enter phone number with country code", null=True,  blank=True)
    email = EmailField(blank=True, null=True, verbose_name="Email")
    date_of_birth = DateField(blank=True, null=True)
    branch = ForeignKey(Branch, on_delete=CASCADE, null=True)
    class Meta:
        default_permissions = () 
        permissions = (
            ("add_staff", "Can add staff"),
            ("accept_request", "Can accept leave request"),
            ("make_request", "can make leave request"),
            ("view_attendance", "can veiw attendance"),
            ("make_attendance", "can make attendance"),
        )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return '%s %s' % (self.username, self.first_name)









