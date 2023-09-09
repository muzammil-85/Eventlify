# Generated by Django 2.2.24 on 2023-08-16 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_paymentrecord_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrecord',
            name='amount',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='event',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='event.EventRecord'),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizer.organizerRecord'),
        ),
        migrations.AlterField(
            model_name='registrationrecord',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Answer'),
        ),
        migrations.AlterField(
            model_name='registrationrecord',
            name='event',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='event.EventRecord'),
        ),
        migrations.AlterField(
            model_name='registrationrecord',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizer.organizerRecord'),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]