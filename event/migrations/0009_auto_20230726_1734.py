# Generated by Django 2.2.24 on 2023-07-26 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20230726_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='email',
        ),
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
