# Generated by Django 2.0.9 on 2018-12-30 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('pending', 'Pending'), ('approved', 'Approved')], default='pending', max_length=255),
        ),
    ]
