# Generated by Django 2.0.9 on 2019-01-28 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.TimeField(blank=True, null=True)),
                ('check_in_date', models.DateField(auto_now=True)),
                ('check_out', models.TimeField(blank=True, null=True)),
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
                ('status', models.CharField(choices=[('rejected', 'Rejected'), ('approved', 'Approved'), ('pending', 'Pending')], default='pending', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Describe your leave request', null=True)),
                ('date_submission', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TypesOfLeave',
            fields=[
                ('leave_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_type', models.CharField(blank=True, max_length=255, null=True)),
                ('total_days', models.IntegerField(default=0)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UserDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_left', models.IntegerField(default=0)),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.TypesOfLeave')),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
