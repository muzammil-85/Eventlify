# Generated by Django 2.2.24 on 2023-07-08 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizerrecord',
            name='Org_id',
        ),
        migrations.AddField(
            model_name='organizerrecord',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
