# Generated by Django 2.2.24 on 2023-07-25 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrationrecord',
            old_name='user',
            new_name='client',
        ),
        migrations.RemoveField(
            model_name='registrationrecord',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='registrationrecord',
            name='category',
        ),
        migrations.RemoveField(
            model_name='registrationrecord',
            name='type',
        ),
    ]
