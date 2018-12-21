# Generated by Django 2.0.9 on 2018-12-20 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.TimeField(auto_now=True)),
                ('check_in_date', models.DateField(auto_now=True)),
                ('check_out', models.TimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('rejected', 'Rejected'), ('pending', 'Pending'), ('approved', 'Approved')], max_length=255, null=True)),
                ('description', models.TextField(blank=True, help_text='Describe your leave request', null=True)),
                ('date_submission', models.DateField(blank=True, null=True)),
                ('responded_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='responded_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TypesOfLeave',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_type', models.CharField(blank=True, choices=[('sick_leave', 'Sick Leave'), ('annual_leave', 'Annual Leave')], max_length=255, null=True)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UserDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_taken', models.IntegerField(default=0)),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.TypesOfLeave')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]