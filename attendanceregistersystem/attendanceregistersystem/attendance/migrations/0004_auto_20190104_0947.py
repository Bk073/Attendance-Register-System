# Generated by Django 2.0.9 on 2019-01-04 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20181230_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=255),
        ),
    ]
