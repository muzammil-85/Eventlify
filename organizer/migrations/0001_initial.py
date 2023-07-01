# Generated by Django 2.2.24 on 2023-07-01 11:20

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
            name='organizerRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=30)),
                ('college_name', models.CharField(max_length=200)),
                ('branch', models.CharField(max_length=10)),
                ('batch_start', models.CharField(max_length=10)),
                ('batch_end', models.CharField(max_length=10)),
                ('number', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
